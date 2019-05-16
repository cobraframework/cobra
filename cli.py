#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from __future__ import with_statement

__author__ = 'Meheret Tesfaye'
__version__ = '0.1.0'
__license__ = 'MIT'

import sys

if __name__ == "__main__":
    try:
        import argparse
    except ImportError:
        print("Please install argparse!")
        sys.exit(0)
    try:
        import textwrap
    except ImportError:
        print("Please install textwrap!")
        sys.exit(0)
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
                             help=' Show this help message and exit')

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

    print(cobra_args)

#     if cobra_args.help:
#         parser.print_help()
#     elif cobra_args.compile and not \
#             cobra_args.more:
#         self.CobraCompile()
#     elif cobra_args.compile and \
#             cobra_args.more:
#         self.CobraCompile(more=True)
#
#     elif cobra_args.migrate and not \
#             cobra_args.more:
#         self.CobraDeploy()
#     elif cobra_args.migrate and \
#             cobra_args.more:
#         self.CobraDeploy(more=True)
#
#     elif cobra_args.deploy and not \
#             cobra_args.more:
#         self.CobraDeploy()
#     elif cobra_args.deploy and \
#             cobra_args.more:
#         self.CobraDeploy(more=True)
#
#     elif cobra_args.test and not \
#             cobra_args.unittest and not cobra_args.pytest:
#         self.CobraUnitTest()
#
#     elif cobra_args.unittest and not \
#             cobra_args.more:
#         self.CobraUnitTest()
#     elif cobra_args.unittest and \
#             cobra_args.more:
#         self.CobraUnitTest(more=True)
#
#     elif cobra_args.pytest and not \
#             cobra_args.more:
#         self.CobraPyTest()
#     elif cobra_args.pytest and \
#             cobra_args.more:
#         self.CobraPyTest()


