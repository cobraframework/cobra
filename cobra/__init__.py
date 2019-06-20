#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# COBRA FRAMEWORK

"""
Cobra is a fast and simple development environment framework for ethereum virtual
machine and it have testing framework for testing smart contract(Solidity file).
all in a single file and with no dependencies other than the
Python Standard Library.

Homepage and documentation: http://cobraframework.github.io

Email: meherett@zoho.com
Copyright (c) 2019, Meheret Tesfaye.
License: MIT (see LICENSE for details)
"""

import pkg_resources
import unittest
import argparse
import os
import sys
import textwrap

from web3 import Web3
from glob import glob
from unittest import TestSuite
from os import makedirs
from colorama import Fore, Style
from pathlib import Path
from eth_tester import EthereumTester
from os.path import join, isdir
from web3.providers.eth_tester import EthereumTesterProvider

from .test.interfaces import Interfaces
from .test import Test
from .project.configuration import Configuration
from .project.migration.deployment import Deployment
from .project.sources.compiler import (
    is_compiled,
    bytecode_link_from_file,
    bytecode_link_to_md5,
    to_compile
)
from .utils.console_log import console_log
from .utils.utils import (
    file_reader,
    file_writer,
    json_loader,
    yaml_loader
)

__all__ = [
    "Configuration",
    "EthereumTester",
    "Fore", "join",
    "Style", "os",
    "TestSuite",
    "EthereumTesterProvider",
    "Deployment",
    "Path", "glob",
    "makedirs", "Web3",
    "isdir", "sys",
    "is_compiled",
    "textwrap",
    "unittest", "Test",
    "Interfaces",
    "argparse",
    "console_log",
    "to_compile",
    "pkg_resources",
    "file_reader",
    "file_writer",
    "json_loader",
    "yaml_loader",
    "bytecode_link_to_md5",
    "bytecode_link_from_file",
]


