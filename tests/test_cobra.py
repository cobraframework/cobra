#!/usr/bin/python3

import os
from pathlib import Path
import pytest
import sys

from cobra.utils import Style, Fore
from cobra.cli.__main__ import main as cli_main


def compile_success_output():
    return Style.DIM + Fore.GREEN + "[SUCCESS]" + Style.RESET_ALL + ' ' + \
           Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
           "ConvertLib.sol done in ./contracts/ConvertLib.json" + "\n" + \
           Style.DIM + Fore.GREEN + "[SUCCESS]" + Style.RESET_ALL + ' ' + \
           Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
           "MetaCoin.sol done in ./contracts/MetaCoin.json" + "\n"


def compile_warning_output():
    return Style.DIM + Fore.YELLOW + "[WARNING]" + Style.RESET_ALL + ' ' + \
           Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
           "ConvertLib.sol already compiled in ./contracts/ConvertLib.json\n" + \
           Style.DIM + Fore.YELLOW + "[WARNING]" + Style.RESET_ALL + ' ' + \
           Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
           "MetaCoin.sol already compiled in ./contracts/MetaCoin.json" + "\n"


@pytest.fixture(scope="module")
def project_path():
    original_path = os.getcwd()
    os.chdir(original_path+"/tests")
    yield Path(original_path+"/tests")
    os.chdir(original_path)


@pytest.fixture(scope="function")
def cli_tester():
    cli_tester = CliTester()
    yield cli_tester
    cli_tester.close()


class CliTester:

    def __init__(self):
        self.argv = sys.argv.copy()

    def __call__(self, argv, *args, **kwargs):
        sys.argv = ['cobra']+argv.split(' ')
        self.args = args
        self.kwargs = kwargs
        cli_main()

    def close(self):
        sys.argv = self.argv


def test_cli_compile(cli_tester, project_path, capsys):
    cli_tester('compile')
    output, error = capsys.readouterr()
    if output != compile_success_output():
        assert output == compile_warning_output()
    else:
        assert output == compile_warning_output()
    cli_tester.close()


# def test_cli_deploy(cli_tester, project_path):
#     cli_tester('deploy')
#     cli_tester.close()
