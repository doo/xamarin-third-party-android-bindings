
from bs4 import BeautifulSoup

from lib.logging_utils import print_error

DEPENDENCY_TAG = 'dependency'

class NuspecBigBoy:

    def __init__(self, nuspec_path):
        try:
            self._xml_file = open(nuspec_path, 'r')
            contents = self._xml_file.read()
            self.nuspec_xml = BeautifulSoup(contents, features="html.parser")
        except Exception as err:
            print_error(f'ERROR: Cannot parse XML at path: {nuspec_path}')
            raise err
    
    def get_nuget_dependencies_dict(self):
        out_dictionary = {}
        dependencies = self.nuspec_xml.find_all(DEPENDENCY_TAG)
        for dependency in dependencies:
            package_name = dependency["id"]
            package_version = dependency["version"]
            out_dictionary[package_name] = package_version
        return out_dictionary
            

    def dispose(self):
        self._xml_file.close()