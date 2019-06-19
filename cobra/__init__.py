#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cobra is a fast and simple development environment framework for ethereum virtual
machine and it have testing framework for testing smart contract(Solidity file).
all in a single file and with no dependencies other than the
Python Standard Library.

Homepage and documentation: http://cobraframework.github.io

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

from cobra.test.interfaces import Interfaces
from cobra.test import Test
from .project.configuration import Configuration
from .project.migration.deployment import Deployment
from .project.sources.compiler import (
    is_compiled,
    bytecode_link_from_file,
    bytecode_link_to_md5,
    to_compile
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
    "unittest",
    "argparse",
    "to_compile",
    "pkg_resources",
    "bytecode_link_to_md5",
    "bytecode_link_from_file",
]


