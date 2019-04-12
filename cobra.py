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


class CobraFramework(CobraConfiguration):

    def __init__(self):
        super().__init__()
        self.cobraCompile = CobraCompile()
        self.cobraNetwork = self.CobraNetwork()
        self.cobraDeploy = CobraDeploy(self.cobraNetwork)

    def CobraArgumentParser(self, argv):
        parser = argparse.ArgumentParser(
            prog="cobra",
            usage="[-h] [help] [compile] [deploy] [migrate] [test {--unittest} or {--pytest}]",
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
                                 help=' Show this help message and exit')
        parser_compile = cobra_parser.add_parser('compile')
        parser_compile.add_argument("compile", action='store_true',
                                    help='compile contract source files')
        parser_migrate = cobra_parser.add_parser('migrate')
        parser_migrate.add_argument(dest="migrate", action='store_true',
                                    help='Alias for deploy')
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
        elif cobra_args.compile:
            self.CobraCompile()

        elif cobra_args.migrate and not \
                cobra_args.more:
            self.CobraDeploy()
        elif cobra_args.migrate and \
                cobra_args.more:
            self.CobraDeploy(more=True)
        elif cobra_args.deploy and not \
                cobra_args.more:
            self.CobraDeploy()
        elif cobra_args.deploy and \
                cobra_args.more:
            self.CobraDeploy(more=True)

        elif cobra_args.test and not \
                cobra_args.unittest and not cobra_args.pytest:
            self.CobraUnitTest()
        elif cobra_args.unittest and not \
                cobra_args.more:
            self.CobraUnitTest()
        elif cobra_args.unittest and \
                cobra_args.more:
            self.CobraUnitTest(more=True)
        elif cobra_args.pytest and not \
                cobra_args.more:
            self.CobraPyTest()
        elif cobra_args.pytest and \
                cobra_args.more:
            self.CobraPyTest()

    def cobra_print(self, text, color=None, bold=False, background=None, underline=False):
        if color == 'success':
            return color_print(text, color='green', bold=bold, highlighter=background, underline=underline)
        elif color == 'warning':
            return color_print(text, color='yellow', bold=bold, highlighter=background, underline=underline)
        elif color == 'error':
            return color_print(text, color='red', bold=bold, highlighter=background, underline=underline)
        else:
            return color_print(text, bold=bold, highlighter=background, underline=underline)

    def CobraCompile(self):
        try:
            read_yaml = self.fileReader("./cobra.yaml")
            load_yaml = self.yamlLoader(read_yaml)
            compile_yaml = load_yaml['compile']
            configurations_yaml = self.compile(compile_yaml)
            for configuration_yaml in configurations_yaml:
                remappings = configuration_yaml['remappings']
                file_path_sol = join(configuration_yaml['solidity_path_dir'], configuration_yaml['solidity'])
                if configuration_yaml['links_path_dir'] is None:
                    cobra_compiled = self.cobraCompile.to_compile(file_path_sol, None, remappings)

                    if not isdir(configuration_yaml['artifact_path_dir']):
                        makedirs(configuration_yaml['artifact_path_dir'])
                    artifact_path_json = join(configuration_yaml['artifact_path_dir'],
                                              str(configuration_yaml['solidity'])[:-4] + ".json")

                    if self.cobraCompile.is_compiled(artifact_path_json, cobra_compiled):
                        self.cobra_print("[WARNING] Cobra: Already compiled in %s" %
                                         artifact_path_json, "warning", bold=True)
                        continue
                    self.cobraCompile.file_writer(artifact_path_json, str(cobra_compiled))
                    self.cobra_print("[SUCCESS] Cobra: Compiled %s" %
                                     artifact_path_json, "success", bold=True)
                else:
                    links_path_dir = str(os.getcwd())
                    for allow_path in configuration_yaml['links_path_dir']:
                        if str(allow_path) == "":
                            links_path_dir = str(os.getcwd())
                        else:
                            links_path_dir = links_path_dir + "," + str(allow_path)

                    cobra_compiled = self.cobraCompile.to_compile(file_path_sol, links_path_dir, remappings)

                    if not isdir(configuration_yaml['artifact_path_dir']):
                        makedirs(configuration_yaml['artifact_path_dir'])
                    artifact_path_json = join(configuration_yaml['artifact_path_dir'],
                                              str(configuration_yaml['solidity'])[:-4] + ".json")

                    if self.cobraCompile.is_compiled(artifact_path_json, cobra_compiled):
                        self.cobra_print("[WARNING] Cobra: Already compiled in %s" %
                                         artifact_path_json, "warning", bold=True)
                        continue
                    self.cobraCompile.file_writer(artifact_path_json, str(cobra_compiled))
                    self.cobra_print("[SUCCESS] Cobra: Compiling %s" %
                                     artifact_path_json, "success", bold=True)
        except KeyError:
            self.cobra_print("[ERROR] Cobra: Can't find compile in cobra.yaml", "error", bold=True)
            sys.exit()

    def CobraDeploy(self, more=None):
        try:
            read_yaml = self.fileReader("./cobra.yaml")
            load_yaml = self.yamlLoader(read_yaml)
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
                        self.cobra_print("[SUCCESS] Cobra: Deploying %s" %
                                         str(configuration_yaml['artifact'])[:-5], "success", bold=True)
                    continue
                else:
                    artifact_path_json = join(configuration_yaml['artifact_path_dir'], configuration_yaml['artifact'])
                    artifact_json = self.cobraDeploy.deploy_with_link(
                        configuration_yaml['artifact_path_dir'],
                        configuration_yaml['artifact'],
                        configuration_yaml['links'], more=more)
                    if artifact_json is not None:
                        self.cobraDeploy.file_writer(artifact_path_json, str(artifact_json))
                        self.cobra_print("[SUCCESS] Cobra: Deploying %s" %
                                         str(configuration_yaml['artifact'])[:-5], "success", bold=True)
                    continue
        except KeyError:
            self.cobra_print("[ERROR] CobraNotFound: Can't find deploy in cobra.yaml", "error", bold=True)
            sys.exit()

    def CobraNetwork(self):
        try:
            read_yaml = self.fileReader("./cobra.yaml")
            load_yaml = self.yamlLoader(read_yaml)
            network_yaml = load_yaml['network']
            configuration_yaml = self.network(network_yaml)
            return configuration_yaml
        except KeyError:
            self.cobra_print("[ERROR] CobraNotFound: Can't find network in cobra.yaml", "error", bold=True)
            sys.exit()

    def CobraUnitTest(self, more=None):
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
                        Path(test_path).resolve(), pattern='*_test.py', top_level_dir=Path(test_path).resolve())
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
                self.cobra_print("[ERROR] CobraNotFound: Can't find test_paths in test", "error", bold=True)
                sys.exit()

        except KeyError:
            self.cobra_print("[ERROR] CobraNotFound: Can't find test in cobra.yaml", "error", bold=True)
            sys.exit()

    def CobraPyTest(self):
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
            self.cobra_print("[ERROR] PyTestNotFound: install pytest framework 'pip install pytest'!",
                             "error", bold=True)
            sys.exit()
        elif not pytest_cobra:
            self.cobra_print("[ERROR] PyTestCobraNotFound: install pytest-cobra 'pip install pytest-cobra'!",
                             "error", bold=True)
            sys.exit()
        try:
            read_yaml = self.fileReader("./cobra.yaml")
            load_yaml = self.yamlLoader(read_yaml)
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
                self.cobra_print("[ERROR] CobraNotFound: Can't find test_paths in test", "error", bold=True)
                sys.exit()

        except KeyError:
            self.cobra_print("[ERROR] CobraNotFound: Can't find test in cobra.yaml", "error", bold=True)
            sys.exit()


if __name__ == "__main__":
    cobraFramework = CobraFramework()
    cobraFramework.CobraArgumentParser(sys.argv[1:])
