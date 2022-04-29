
# This is a Python wrapper around the NuFetch .NET project
# The NuFetch project was carefully stolen from the internet and modified to serve our purpose,
# which is retrieving the list of every transient and non-transient dependency of
# a given NuGet package.
# 
# If you have any questions about this, you can ask Rutkay at any time, day and night, seven days a week.
#
# Made by "Not Marco" on 29/04/2022
#
# @ Some Rights Reserved @
#

import subprocess
import os
from sys import stderr
import time

NU_FETCH_PATH = "lib/NuFetch"
OUPTUT_FOLDER = "output"
EXECUTABLE_PATH = "src/NuFetch/bin/Debug/NuFetch.exe"
VERSION_SEPARATOR = "@"
OS_SLEEP_TIME = 1 # Seconds
HIDE_LOGS = True

def system_call(command):
    if (HIDE_LOGS):
        os.system(f'{command} >/dev/null')
    else:
        os.system(command)

# Fetches the dependencies for the given package, and returns a dictionary with (package_name: package_version) entries
def fetch_dependencies(package_name, package_version):

    # If the dependencies file was previously generated, we can use it without running NuFetch again (Advanced Spacial Cross Platform Crossfit Cache Mechanism)
    deps_file = get_dependencies_dictionary(
        package_name = package_name, 
        package_version = package_version
    )
    if deps_file is not None:
        return deps_file

    # Launches the NuFetch executable to retrieve all the dependencies for the given package.
    # The output will be located in the $NU_FETCH_PATH/output folder
    executable_path = os.path.join(NU_FETCH_PATH, EXECUTABLE_PATH)
    system_call(f"mono {executable_path} -p {package_name} -v {package_version} --fetchOnly")
    time.sleep(OS_SLEEP_TIME)

    # Hands it over to the get_dependencies_dictionary expert, to create the dict of dependencies from the
    # file we just generated
    return get_dependencies_dictionary(
        package_name = package_name, 
        package_version = package_version
    )

# Creates a dictionary from the autogenerated dependencies text file 
def get_dependencies_dictionary(package_name, package_version):

    # Builds complete path for list of dependencies text file
    file_name = file_name_for_package(package_name, package_version)
    file_path = os.path.join(NU_FETCH_PATH, OUPTUT_FOLDER, file_name)
    if not os.path.exists(file_path):
        return None

    # Reads dependencies text file into 'packages'
    packages = []
    try:
        with open(file_path) as file:
            packages = file.read().splitlines()
    except Exception as err:
        print(f"Cannot find dependencies text file at {file_path}")
        raise err

    out_dictionary = {}
    for package in packages:
        parts = package.split(VERSION_SEPARATOR)
        name = parts[0]
        version = parts[1]
        out_dictionary[name] = version

    return out_dictionary
    
# Returns the dependencies text file name for the given package. 
# Matches the format of the output file, as specified in the NuFetch project.
def file_name_for_package(package_name, package_version):
    return f'package_{package_name}_{package_version}.txt'