
from datetime import datetime
import json
import os
from sqlite3 import Date
from lib import nufetch_wrapper as NuFetch
from lib.nuspec_helper import NuspecBigBoy
from lib.logging_utils import print_big_bad_bold_error, print_big_boy_warning, print_error, print_success, print_bold, print_warning
from tqdm import tqdm
from packaging.version import parse as parse_version

XAMARIN_FORMS_VERSION = '5.0.0.2401'
ONLY_CHECK_DOWNGRADES = True
NUSPEC_PATH = "Scanbot.Xamarin.SDK.Dependencies.nuspec"
REPORT_FILE_NAME = 'compatibility_report'
REPORT_FILE_PATH = 'reports'

# ---------------------------------------------------------------
#                             MAIN
# ---------------------------------------------------------------

# ->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->-> 
# 1) Retrieve the dependency tree for the version of Xamarin Forms specified on top of this script
# ->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
print(f"Retrieving dependencies for Xamarin Forms v{XAMARIN_FORMS_VERSION}\n")
forms_dependencies = NuFetch.fetch_dependencies('Xamarin.Forms', XAMARIN_FORMS_VERSION)
if forms_dependencies is None:
    print_error(f"An error occured while retrieving dependencies for Xamarin Forms v{XAMARIN_FORMS_VERSION}")
    exit(-1)

print_success(f"\nDependencies fetched correctly for Xamarin Forms v{XAMARIN_FORMS_VERSION}\n")

print("\nLoading your nuspec file...")

# ->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->-> 
# 2) Load Dependencies nuspec file, and retrieve a dictionary of dependencies, 
#    in the same format as in the previous step
# ->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->-> 
nuspec = NuspecBigBoy(NUSPEC_PATH)
nuspec_dependencies = nuspec.get_nuget_dependencies_dict()
nuspec.dispose()
print_success(f"\nNuspec dependencies loaded correctly!\n")

# ->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->-> 
# 3) For each .nuspec dependency, we retrieve transient and non-transient dependencies,
#    using NuFetch again
# ->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->-> 
print("\nFetching dependencies for each nuspec dependency...\n")
pbar_keys = tqdm(
    [key for key in nuspec_dependencies],
    colour='green',
    bar_format='{l_bar}:{bar}'
)
nuspec_transient_dependencies = {}
for package in pbar_keys:
    version = nuspec_dependencies[package]
    pbar_keys.set_description(f'{package} v{version}')
    fetched_dependencies = NuFetch.fetch_dependencies(package, version)
    nuspec_transient_dependencies[f"{package}@{version}"] = fetched_dependencies

print_success(f"\nNuspec dependencies FETCHED correctly!\n")

# ->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->-> 
# 4) Now we can finally compare the .nuspec dependencies with the Xamarin Forms dependencies,
#    by iterating the latest dictionary, dependency by dependency, trying to find a match
#    with the Xamarin Forms's ones; the result of this process would be a report on which dependencies
#    match but have different versions
# ->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->-> 

def check_compatibility(package_name, package_version, is_transient=True):
    if package_name not in forms_dependencies:
        return None
    forms_version = forms_dependencies[package_name]

    parsed_forms_version = parse_version(forms_version)
    parsed_package_version = parse_version(package_version)

    if parsed_forms_version != parsed_package_version:
        if parsed_forms_version < parsed_package_version and ONLY_CHECK_DOWNGRADES:
            return None

        symbol = '-' if is_transient else '*'
        type = 'transient' if is_transient else 'MAIN'
        return f"{symbol} {type} dependency {package_name} v{package_version} conflict: {package_name} v{forms_version}", is_transient

# The format will be 'package@version': [ reports ]
compatibility_report = {}
main_conflicts_count = 0
transient_conflicts_count = 0

for package in nuspec_transient_dependencies:
    compatibility_report[package] = []

    # Check Main Dependency Compatibility
    parts = package.split('@')
    name = parts[0]
    version = parts[1]
    report = check_compatibility(package_name=name, package_version=version, is_transient=False)
    if report is not None:
        main_conflicts_count += 1
        compatibility_report[package].append(report)

    # Check Transient Dependencies Compatibility
    package_dependencies = nuspec_transient_dependencies[package]
    for dependency_name in package_dependencies:
        dependency_version = package_dependencies[dependency_name]
        report = check_compatibility(package_name=dependency_name, package_version=dependency_version)
        if report is not None:
            transient_conflicts_count += 1
            compatibility_report[package].append(report)

# Print the results
any_errors = False
lines = []
for package in nuspec_transient_dependencies:
    package_report = compatibility_report[package]
    print_bold(f"\nCompatibility for {package}:\n")

    if len(package_report) > 0:
        lines.append(f"\n\nCompatibility report for {package}:\n")
        for report, is_transient in package_report:
            any_errors = True
            if not is_transient:
                print_big_bad_bold_error(f'\n  {report}')
            else:
                print_warning(f'\n  {report}')
            lines.append(f'\n  {report}')
        print()
    else:
        print_success(f"  > {package} is compatible with Xamarin Forms v{XAMARIN_FORMS_VERSION}!")

print("\n")
if any_errors:
    if main_conflicts_count == 0:
        print_big_boy_warning(f"The compatibility check passed, but with {transient_conflicts_count} transient dependencies conflicts that you should take a look at.")
    else:
        print_error(f"The compatibility check failed with {main_conflicts_count} main dependency errors and {transient_conflicts_count} transient dependencies errors.\nUse the report to address the issues.")
        print_big_bad_bold_error("\nMain Problems:\n")
        for package_key in compatibility_report:
            for report, is_transient in compatibility_report[package_key]:
                if not is_transient:
                    print_error(report)
            
                
    now = datetime.now()
    
    line_timestamp = now.strftime("%Y-%m-%d %H:%M:%S %z")
    lines.insert(0, f'with Xamarin Forms version v{XAMARIN_FORMS_VERSION} and .nuspec packages:\n' +  
        json.dumps(nuspec_dependencies, sort_keys=False, indent=4) + "\n"
    )
    lines.insert(0, f'Report made at {line_timestamp}')

    file_timestamp = now.strftime("%Y_%m_%d-%I_%M_%S_%p")
    report_file_name = f'{REPORT_FILE_NAME}_{file_timestamp}.txt'
    report_file_path = os.path.join(REPORT_FILE_PATH, report_file_name)

    with open(report_file_path, 'w+') as f:
        f.writelines(lines)
    
    print_bold(f"\nThe report has been saved in {report_file_path}.\n")

else:
    print_success("The compatibility check ended with SUCCESS!\nGo ahead and spread this Xamarin disease everywhere!")

print("Done.\n")