#!/usr/bin/python3

import os
from pathlib import Path
import pytest
import sys

from cobra.cli.__main__ import main as cli_main


@pytest.fixture(scope="module")
def project_path():
    original_path = os.getcwd()
    os.chdir(original_path + "/tests")
    yield Path(original_path + "/tests")
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

