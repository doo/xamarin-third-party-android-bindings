
import json

from colorama import Fore, Style

NOW_I_AM_BOLD = '\033[1m'
NOW_I_AM_NOT = '\033[0m'

def print_error(text):
    print(f'{Fore.RED}{text}{Style.RESET_ALL}')

def print_big_bad_bold_error(text):
    print(f'{NOW_I_AM_BOLD}{Fore.RED}{text}{Style.RESET_ALL}{NOW_I_AM_NOT}')

def print_success(text):
    print(f'{Fore.GREEN}{text}{Style.RESET_ALL}')

def print_warning(text):
    print(f'{Fore.YELLOW}{text}{Style.RESET_ALL}')

def print_big_boy_warning(text):
    print(f'{NOW_I_AM_BOLD}{Fore.YELLOW}{text}{Style.RESET_ALL}{NOW_I_AM_NOT}')

def print_bold(text):
    print(f'{NOW_I_AM_BOLD}{text}{NOW_I_AM_NOT}')

def print_dictionary(dict):
    print(json.dumps(dict, sort_keys=False, indent=4))
