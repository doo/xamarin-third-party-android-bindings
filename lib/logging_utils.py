
import json

from colorama import Fore, Style

def print_error(text):
    print(f'{Fore.RED}{text}{Style.RESET_ALL}')

def print_success(text):
    print(f'{Fore.GREEN}{text}{Style.RESET_ALL}')

def print_bold(text):
    print(f'\033[1m{text}\033[0m')

def print_dictionary(dict):
    print(json.dumps(dict, sort_keys=False, indent=4))
