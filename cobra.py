from web3.providers.eth_tester import EthereumTesterProvider
from configuration import CobraConfiguration
from test.interfaces import CobraInterfaces
from lazyme.string import color_print
from eth_tester import EthereumTester
from compile import CobraCompile
from os.path import join, isdir
from unittest import TestSuite
from deploy import CobraDeploy
from test import CobraTest
from pathlib import Path
from os import makedirs
from glob import glob
from web3 import Web3
import pkg_resources
import argparse
import unittest
import textwrap
import sys
import os


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
        # Cobra Agreements
        cobra_args = parser.parse_args()

        if cobra_args.help:
            parser.print_help()
        elif cobra_args.compile:
            self.CobraCompile()
        elif cobra_args.migrate:
            self.CobraDeploy()
        elif cobra_args.deploy:
            self.CobraDeploy()
        elif cobra_args.test and not \
                cobra_args.unittest and not cobra_args.pytest:
            self.CobraUnitTest()
        elif cobra_args.unittest:
            self.CobraUnitTest()
        elif cobra_args.pytest:
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
            read_yaml = self.file_reader("./cobra.yaml")
            load_yaml = self.yaml_loader(read_yaml)
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



