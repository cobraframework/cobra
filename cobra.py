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

from test import CobraInterfaces
from colorama import Fore, Style
from configuration import CobraConfiguration
from eth_tester import EthereumTester
from unittest import TestSuite
from web3.providers.eth_tester import EthereumTesterProvider
from test import CobraTest
from deploy import CobraDeploy
from lazyme.string import color_print
from os.path import join, isdir
import sys
from pathlib import Path
from os import makedirs
from compile import CobraCompile
from glob import glob
import textwrap
import pkg_resources
import os
from web3 import Web3
import unittest
import argparse


def CobraArgumentParser(argv):
    parser = argparse.ArgumentParser(
        prog="cobra",
        usage="[-h] [help] [compile {--more}] [deploy {--more}] [migrate {--more}] "
              "[test {--unittest} or {--pytest}, {--more}]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
                    --------------------
                    !!!PLEASE HELP ME!!!
                    --------------------
        Donate in Bitcoin: 3JiPsp6bT6PkXF3f9yZsL5hrdQwtVuXXAk
        Donate in Ethereum: 0xD32AAEDF28A848e21040B6F643861A9077F83106
        '''),
        description=textwrap.dedent('''\
        Cobra Framework is a world class development environment, testing framework and
        asset pipeline for blockchains using the Ethereum Virtual Machine (EVM), aiming
        to make life as a developer easier.   https://github.com/cobraframework'''))

    parser.set_defaults(compile=False, deploy=False, migrate=False,
                        test=False, unittest=False, pytest=False, help=False)

    cobra_parser = parser.add_subparsers(
        title="COBRA FRAMEWORK",
        description=textwrap.dedent('''\
                    Cobra commands list below here!'''))

    parser_help = cobra_parser.add_parser('help')
    parser_help.add_argument("help", action='store_true',
                             help='Show this help message and exit')

    parser_compile = cobra_parser.add_parser('compile')
    parser_compile.add_argument("compile", action='store_true',
                                help='compile contract source files')
    parser_compile.add_argument('-m', '--more', action='store_true',
                                help='View more errors [compile]')

    parser_migrate = cobra_parser.add_parser('migrate')
    parser_migrate.add_argument(dest="migrate", action='store_true',
                                help='Alias for deploy')
    parser_migrate.add_argument('-m', '--more', action='store_true',
                                help='View more errors [migrate]')

    parser_deploy = cobra_parser.add_parser('deploy')
    parser_deploy.add_argument("deploy", action='store_true',
                               help='Run deploy to deploy compiled contracts')
    parser_deploy.add_argument('-m', '--more', action='store_true',
                               help='View more errors [deploy]')

    parser_test = cobra_parser.add_parser('test')
    parser_test.add_argument("test", action='store_true',
                             help="Run Python test by default [Unittest]. There are two types of testing framework "
                                  "Unittest and Pytest. Unittest https://docs.python.org/3/library/unittest.html "
                                  "and Pytest https://docs.pytest.org/en/latest/")
    parser_test.add_argument('-u', '--unittest', action='store_true',
                             help='Run Python builtin tests vie [Unittest]')
    parser_test.add_argument('-p', '--pytest', action='store_true',
                             help='Run Python tests vie [PyTest] but, First install pytest and plugin pytest-cobra '
                                  'using pip [pip install pytest-cobra] '
                                  'or https://github.com/cobraframework/pytest-cobra')
    parser_test.add_argument('-m', '--more', action='store_true',
                             help='View more errors [test]')
    # Cobra Agreements
    cobra_args = parser.parse_args()

    if cobra_args.help:
        parser.print_help()
    elif cobra_args.compile and not \
            cobra_args.more:
        cobraFramework = CobraFramework(more=False)
        cobraFramework.CobraCompile(more=False)
    elif cobra_args.compile and \
            cobra_args.more:
        cobraFramework = CobraFramework(more=True)
        cobraFramework.CobraCompile(more=True)

    elif cobra_args.migrate and not \
            cobra_args.more:
        cobraFramework = CobraFramework(more=False)
        cobraFramework.CobraDeploy(more=False)
    elif cobra_args.migrate and \
            cobra_args.more:
        cobraFramework = CobraFramework(more=True)
        cobraFramework.CobraDeploy(more=True)

    elif cobra_args.deploy and not \
            cobra_args.more:
        cobraFramework = CobraFramework(more=False)
        cobraFramework.CobraDeploy(more=False)
    elif cobra_args.deploy and \
            cobra_args.more:
        cobraFramework = CobraFramework(more=True)
        cobraFramework.CobraDeploy(more=True)

    elif cobra_args.test and not cobra_args.unittest\
            and not cobra_args.pytest and not cobra_args.more:
        cobraFramework = CobraFramework(more=False)
        cobraFramework.CobraUnitTest(more=False)

    elif cobra_args.test and not cobra_args.unittest\
            and not cobra_args.pytest and cobra_args.more:
        cobraFramework = CobraFramework(more=True)
        cobraFramework.CobraUnitTest(more=True)

    elif cobra_args.unittest and not \
            cobra_args.more:
        cobraFramework = CobraFramework(more=False)
        cobraFramework.CobraUnitTest(more=False)
    elif cobra_args.unittest and \
            cobra_args.more:
        cobraFramework = CobraFramework(more=True)
        cobraFramework.CobraUnitTest(more=True)

    elif cobra_args.pytest and not \
            cobra_args.more:
        cobraFramework = CobraFramework(more=False)
        cobraFramework.CobraPyTest(more=False)
    elif cobra_args.pytest and \
            cobra_args.more:
        cobraFramework = CobraFramework(more=True)
        cobraFramework.CobraPyTest(more=True)
    parser.exit()


class CobraFramework(CobraConfiguration):

    def __init__(self, more=False):
        super().__init__()
        self.cobraCompile = CobraCompile(more)
        self.cobraNetwork = self.CobraNetwork(more)
        self.cobraDeploy = CobraDeploy(self.cobraNetwork, more)

    def CobraCompile(self, more=False):
        try:
            read_yaml = self.fileReader("./cobra.yaml")
            load_yaml = self.yamlLoader(read_yaml, more=more)
            compile_yaml = load_yaml['compile']
            configurations_yaml = self.compile(compile_yaml)
            for configuration_yaml in configurations_yaml:
                import_remappings = configuration_yaml['import_remappings']
                file_path_sol = join(configuration_yaml['solidity_path_dir'], configuration_yaml['solidity'])
                if configuration_yaml['allow_paths'] is None:
                    cobra_compiled = self.cobraCompile.to_compile(file_path_sol, None,
                                                                  import_remappings, more=more)

                    if not isdir(configuration_yaml['artifact_path_dir']):
                        makedirs(configuration_yaml['artifact_path_dir'])
                    solidity_name = str(configuration_yaml['solidity'])
                    artifact_path_json = join(configuration_yaml['artifact_path_dir'],
                                              solidity_name[:-4] + ".json")

                    if self.cobraCompile.is_compiled(artifact_path_json, cobra_compiled):
                        self.cobra_print("%s already compiled in %s" %
                                         (solidity_name, artifact_path_json), "warning", "Compile")
                        continue
                    self.cobraCompile.file_writer(artifact_path_json, str(cobra_compiled))
                    self.cobra_print("%s done in %s" %
                                     (solidity_name, artifact_path_json), "success", "Compile")
                else:
                    allow_paths = str()
                    for allow_path in configuration_yaml['allow_paths']:
                        if str(allow_path) == "":
                            allow_paths = allow_path
                        else:
                            allow_paths = allow_paths + "," + str(allow_path)

                    cobra_compiled = self.cobraCompile.to_compile(file_path_sol,
                                                                  allow_paths, import_remappings, more)

                    if not isdir(configuration_yaml['artifact_path_dir']):
                        makedirs(configuration_yaml['artifact_path_dir'])
                    solidity_name = str(configuration_yaml['solidity'])
                    artifact_path_json = join(configuration_yaml['artifact_path_dir'],
                                              solidity_name[:-4] + ".json")

                    if self.cobraCompile.is_compiled(artifact_path_json, cobra_compiled):
                        self.cobra_print("%s already compiled in %s" %
                                         (solidity_name, artifact_path_json), "warning", "Compile")
                        continue
                    self.cobraCompile.file_writer(artifact_path_json, str(cobra_compiled))
                    self.cobra_print("%s done in %s" %
                                     (solidity_name, artifact_path_json), "success", "Compile")
        except KeyError:
            self.cobra_print("compile in cobra.yaml", "error", "NotFound")
            sys.exit()

    def CobraDeploy(self, more=False):
        try:
            read_yaml = self.fileReader("./cobra.yaml")
            load_yaml = self.yamlLoader(read_yaml, more=more)
            deploy_yaml = load_yaml['deploy']
            configurations_yaml = self.deploy(deploy_yaml)
            # self.cobraDeploy.display_account()
            for configuration_yaml in configurations_yaml:
                if configuration_yaml['links'] is None:
                    artifact_path_json = join(configuration_yaml['artifact_path_dir'], configuration_yaml['artifact'])
                    artifact_json = self.cobraDeploy.deploy_with_out_link(
                        configuration_yaml['artifact_path_dir'],
                        configuration_yaml['artifact'], more=more)
                    if artifact_json is not None:
                        self.cobraDeploy.file_writer(artifact_path_json, str(artifact_json))
                    continue
                else:
                    artifact_path_json = join(configuration_yaml['artifact_path_dir'], configuration_yaml['artifact'])
                    artifact_json = self.cobraDeploy.deploy_with_link(
                        configuration_yaml['artifact_path_dir'],
                        configuration_yaml['artifact'],
                        configuration_yaml['links'], more=more)
                    if artifact_json is not None:
                        self.cobraDeploy.file_writer(artifact_path_json, str(artifact_json))
                    continue
        except KeyError:
            self.cobra_print("deploy in cobra.yaml", "error", "NotFound")
            sys.exit()

    def CobraNetwork(self, more=False):
        try:
            read_yaml = self.fileReader("./cobra.yaml")
            load_yaml = self.yamlLoader(read_yaml, more=more)
            network_yaml = load_yaml['network']
            configuration_yaml = self.network(network_yaml)
            return configuration_yaml
        except KeyError:
            self.cobra_print("network in cobra.yaml", "error", "NotFound")
            sys.exit()

    def CobraUnitTest(self, more=False):
        """
        Start testing Cobra using Unittest to test Smart Contract (Solidity file)

        The unittest unit testing framework was originally inspired by JUnit and has
        a similar flavor as major unit testing frameworks in other languages. It supports
        test automation, sharing of setup and shutdown code for tests, aggregation of
        tests into collections, and independence of the tests from the reporting framework.
        :return:
        """

        # Collection of test cases
        testSuite = TestSuite()
        testCaseClasses = []

        # Initializing ethereum tester
        _ethereumTester = EthereumTester()
        # Initializing ethereum tester provider
        _ethereumTesterProvider = EthereumTesterProvider(_ethereumTester)
        # Initializing web3 added ethereum tester provider
        _web3 = Web3(_ethereumTesterProvider)

        def zero_gas_price_strategy(web3, transaction_params=None):
            # zero gas price makes testing simpler.
            return 0

        # Set gas price strategy
        _web3.eth.setGasPriceStrategy(zero_gas_price_strategy)
        # Initializing cobra interfaces
        cobraInterfaces = CobraInterfaces(_web3, "./cobra.yaml", more)

        class CollectionInterfaces:
            web3 = _web3
            ethereumTester = _ethereumTester
            compiledInterfaces = cobraInterfaces.getInterfaces()

        try:
            read_yaml = self.fileReader("./cobra.yaml")
            load_yaml = self.yamlLoader(read_yaml)
            test_yaml = load_yaml['test']
            try:
                test_paths = test_yaml['test_paths']
                for test_path in test_paths:
                    test_loader = unittest.defaultTestLoader.discover(
                        Path(test_path).resolve(), pattern='*_test.py',
                        top_level_dir=Path(test_path).resolve())
                    for all_test_suite in test_loader:
                        for test_suites in all_test_suite:
                            for test_suite in test_suites:
                                testCaseClasses.append(test_suite.__class__)

                # Added test case class on test suite array
                for testCaseClass in list(set(testCaseClasses)):
                    testSuite.addTest(CobraTest.cobra(testCaseClass,
                                                      collectionInterfaces=CollectionInterfaces()))
                # Run Unittest
                unittest.TextTestRunner(verbosity=2).run(testSuite)

            except KeyError:
                self.cobra_print("test_paths in test", "error", "NotFound")
                sys.exit()

        except KeyError:
            self.cobra_print("test in cobra.yaml", "error", "NotFound")
            sys.exit()

    def CobraPyTest(self, more=False):
        pytest = False
        pytest_cobra = False
        installed_packages = pkg_resources.working_set
        package_keys = sorted(['%s' % installed_package.key
                               for installed_package in installed_packages])
        for package_key in package_keys:
            if package_key == 'pytest':
                pytest = True
            elif package_key == 'pytest-cobra':
                pytest_cobra = True
            else:
                pass

        if not pytest:
            self.cobra_print("Install pytest framework 'pip install pytest'!",
                             "error", "NotFound")
            sys.exit()
        elif not pytest_cobra:
            self.cobra_print("Install pytest-cobra 'pip install pytest-cobra'!",
                             "error", "NotFound")
            sys.exit()
        try:
            read_yaml = self.fileReader("./cobra.yaml")
            load_yaml = self.yamlLoader(read_yaml, more=more)
            test_yaml = load_yaml['test']
            try:
                _test = ['--cobra', 'cobra.yaml']
                test_paths = test_yaml['test_paths']
                for test_path in test_paths:
                    tests = glob(join(Path(test_path).resolve(), "*_test.py"))
                    for test in tests:
                        _test.append(test)
                __import__("pytest").main(_test)
            except KeyError:
                self.cobra_print("test_paths in test", "error", "NotFound")
                sys.exit()

        except KeyError:
            self.cobra_print("test in cobra.yaml", "error", "NotFound")
            sys.exit()


if __name__ == "__main__":
    CobraArgumentParser(sys.argv[1:])
