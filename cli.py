#!/usr/bin/env python
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

from __future__ import with_statement

__author__ = 'Meheret Tesfaye'
__version__ = '0.1.0'
__license__ = 'MIT'
__epilog__ = '''\
                            --------------------
                            !!!PLEASE HELP ME!!!
                            --------------------
                Donate in Bitcoin: 3JiPsp6bT6PkXF3f9yZsL5hrdQwtVuXXAk
                Donate in Ethereum: 0xD32AAEDF28A848e21040B6F643861A9077F83106
                '''
__description__ = '''\
                Cobra Framework is a world class development environment, testing framework and
                asset pipeline for blockchains using the Ethereum Virtual Machine (EVM), aiming 
                to make life as a developer easier.   https://github.com/cobraframework'''

# Python builtin libraries
import os
import sys
import re
from os.path import basename

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
        epilog=textwrap.dedent(__epilog__),
        description=textwrap.dedent(__description__))

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


def cobraPrint(text, color=None, bold=False, background=None, underline=False):
    try:
        from lazyme.string import cobraPrint
    except ImportError:
        print("Please install lazyme!")
        sys.exit(0)
    if color == 'success':
        return cobraPrint(text, color='green', bold=bold, highlighter=background, underline=underline)
    elif color == 'warning':
        return cobraPrint(text, color='yellow', bold=bold, highlighter=background, underline=underline)
    elif color == 'error':
        return cobraPrint(text, color='red', bold=bold, highlighter=background, underline=underline)
    else:
        return cobraPrint(text, bold=bold, highlighter=background, underline=underline)


# File reader
def fileReader(file, _=None):
    try:
        with open(file, 'r') as read_file:
            return_file = read_file.read()
            read_file.close()
            return return_file
    except FileNotFoundError:
        if _ == "false": return False
        elif _ == "true": return True
        else:
            cobraPrint("[Cobra] FileNotFound: %s" % file, "error", bold=True)
            sys.exit()


# File writer
def fileWriter(file_path, docs):
    with open(file_path, 'w') as write_file:
        write_file.write(docs)
        write_file.close()
        return


# YAML file loader
def yamlLoader(yaml_file, _=None):
    try:
        import yaml
        from yaml import load
    except ImportError:
        cobraPrint("Please install yaml!", "error")
        sys.exit()
    try:
        load_compile = load(yaml_file)
        return load_compile
    except yaml.scanner.ScannerError as scannerError:
        if _ == "false": return False
        elif _ == "true": return True
        else:
            cobraPrint("[Cobra] YAMLScannerError: %s" % scannerError, "error", bold=True)
            sys.exit()


# JSON file loader
def jsonLoader(json_file, _=None):
    try:
        import json
        from json import loads
    except ImportError:
        cobraPrint("Please install json!", "error")
        sys.exit()
    try:
        loaded_json = loads(json_file)
        return loaded_json
    except json.decoder.JSONDecodeError as jsonDecodeError:
        if _ == "false": return False
        elif _ == "true": return True
        else:
            cobraPrint("[Cobra] JSONDecodeError: %s" % jsonDecodeError, "error", bold=True)
            sys.exit()


class Configuration:

    def __init__(self):
        pass

    def hasRemapping(self, contract):
        # Finding remappings and checking not None
        if 'remappings' in contract and \
                contract['remappings']:
            return True
        # Finding remappings and checking None
        elif 'remappings' in contract and \
                not contract['remappings']:
            return False
        else:
            return False

    def hasSolidityPathDir(self, contract):
        # Finding solidity path dir and checking not None
        if 'solidity_path_dir' in contract and \
                contract['solidity_path_dir']:
            return True
        # Finding solidity path dir and checking None
        elif 'solidity_path_dir' in contract and \
                not contract['solidity_path_dir']:
            return False
        else:
            return False

    def hasLinksPathDir(self, contract):
        # Finding links path dir on contract checking not None
        if 'links_path_dir' in contract and \
                contract['links_path_dir']:
            return True
        # Finding links path dir on contract checking None
        elif 'links_path_dir' in contract and \
                not contract['links_path_dir']:
            return False
        else:
            return False

    def compile(self, compile_yaml):
        compiles = []

        # Finding solidity path directory
        if 'solidity_path_dir' in compile_yaml:
            # Finding contracts array
            if 'contracts' in compile_yaml:
                # Checking artifact path directory
                if 'artifact_path_dir' in compile_yaml:
                    artifact_path_dir = compile_yaml['artifact_path_dir']
                else:
                    artifact_path_dir = "./build/contracts"
                    cobraPrint("[WARNING] Checking: Can't find artifact_path_dir on compile. "
                               "by default uses './build/contracts'", bold=True)
                # Looping contracts
                for contract in compile_yaml['contracts']:
                    # Finding solidity on contract
                    if 'solidity' in contract['contract']:
                        if self.hasLinksPathDir(contract['contract']):
                            if self.hasSolidityPathDir(contract['contract']):
                                if self.hasRemapping(contract['contract']):
                                    compiles.append(dict(
                                        solidity_path_dir=contract['contract']['solidity_path_dir'],
                                        solidity=contract['contract']['solidity'],
                                        links_path_dir=contract['contract']['links_path_dir'],
                                        artifact_path_dir=artifact_path_dir,
                                        remappings=contract['contract']['remappings']
                                    ))
                                    continue
                                else:
                                    compiles.append(dict(
                                        solidity_path_dir=contract['contract']['solidity_path_dir'],
                                        solidity=contract['contract']['solidity'],
                                        links_path_dir=contract['contract']['links_path_dir'],
                                        artifact_path_dir=artifact_path_dir,
                                        remappings=None
                                    ))
                                    continue
                            else:
                                if self.hasRemapping(contract['contract']):
                                    compiles.append(dict(
                                        solidity_path_dir=compile_yaml['solidity_path_dir'],
                                        solidity=contract['contract']['solidity'],
                                        links_path_dir=contract['contract']['links_path_dir'],
                                        artifact_path_dir=artifact_path_dir,
                                        remappings=contract['contract']['remappings']
                                    ))
                                    continue
                                else:
                                    compiles.append(dict(
                                        solidity_path_dir=compile_yaml['solidity_path_dir'],
                                        solidity=contract['contract']['solidity'],
                                        links_path_dir=contract['contract']['links_path_dir'],
                                        artifact_path_dir=artifact_path_dir,
                                        remappings=None
                                    ))
                                    continue
                        else:
                            if self.hasSolidityPathDir(contract['contract']):
                                if self.hasRemapping(contract['contract']):
                                    compiles.append(dict(
                                        solidity_path_dir=contract['contract']['solidity_path_dir'],
                                        solidity=contract['contract']['solidity'],
                                        links_path_dir=None,
                                        artifact_path_dir=artifact_path_dir,
                                        remappings=contract['contract']['remappings']
                                    ))
                                    continue
                                else:
                                    compiles.append(dict(
                                        solidity_path_dir=contract['contract']['solidity_path_dir'],
                                        solidity=contract['contract']['solidity'],
                                        links_path_dir=None,
                                        artifact_path_dir=artifact_path_dir,
                                        remappings=None
                                    ))
                                    continue
                            else:
                                if self.hasRemapping(contract['contract']):
                                    compiles.append(dict(
                                        solidity_path_dir=compile_yaml['solidity_path_dir'],
                                        solidity=contract['contract']['solidity'],
                                        links_path_dir=None,
                                        artifact_path_dir=artifact_path_dir,
                                        remappings=contract['contract']['remappings']
                                    ))
                                    continue
                                else:
                                    compiles.append(dict(
                                        solidity_path_dir=compile_yaml['solidity_path_dir'],
                                        solidity=contract['contract']['solidity'],
                                        links_path_dir=None,
                                        artifact_path_dir=artifact_path_dir,
                                        remappings=None
                                    ))
                                    continue
                    else:
                        cobraPrint("[ERROR] CobraNotFound: Can't find solidity in contract.",
                                   "error", bold=True)
                        sys.exit()
            else:
                cobraPrint("[ERROR] CobraNotFound: Can't find contracts in compile [cobra.yaml]",
                           "error", bold=True)
                sys.exit()
        else:
            cobraPrint("[ERROR] Cobra: Can't find solidity_path_dir in compile [cobra.yaml]",
                       "error", bold=True)
            sys.exit()

        return compiles

    def deploy(self, deploy_yaml):
        deploys = []

        if 'artifact_path_dir' in deploy_yaml:
            if 'contracts' in deploy_yaml:
                for contract in deploy_yaml['contracts']:

                    if 'artifact' in contract['contract']:
                        if 'links' in contract['contract']:
                            if contract['contract']['links']:
                                deploys.append(dict(
                                    artifact_path_dir=deploy_yaml['artifact_path_dir'],
                                    artifact=contract['contract']['artifact'],
                                    links=contract['contract']['links']
                                ))
                                continue
                            elif not contract['contract']['links']:
                                deploys.append(dict(
                                    artifact_path_dir=deploy_yaml['artifact_path_dir'],
                                    artifact=contract['contract']['artifact'],
                                    links=None
                                ))
                                continue
                        else:
                            deploys.append(dict(
                                artifact_path_dir=deploy_yaml['artifact_path_dir'],
                                artifact=contract['contract']['artifact'],
                                links=None
                            ))
                            continue
                    else:
                        cobraPrint("[ERROR] CobraNotFound: Can't find artifact in contract.", "error", bold=True)
                        sys.exit()
            else:
                cobraPrint(
                    "[ERROR] CobraNotFound: Can't find contracts in deploy", "error", bold=True)
                sys.exit()
        else:
            cobraPrint(
                "[ERROR] CobraNotFound: Can't find artifact_path_dir in deploy", "error", bold=True)
            sys.exit()

        return deploys

    def test(self, test_yaml):
        tests = []

        if 'artifact_path_dir' in test_yaml:
            if 'contracts' in test_yaml:
                for contract in test_yaml['contracts']:

                    if 'artifact' in contract['contract']:
                        if 'links' in contract['contract']:
                            if contract['contract']['links']:
                                tests.append(dict(
                                    artifact_path_dir=test_yaml['artifact_path_dir'],
                                    artifact=contract['contract']['artifact'],
                                    links=contract['contract']['links']
                                ))
                                continue
                            elif not contract['contract']['links']:
                                tests.append(dict(
                                    artifact_path_dir=test_yaml['artifact_path_dir'],
                                    artifact=contract['contract']['artifact'],
                                    links=None
                                ))
                                continue
                        else:
                            tests.append(dict(
                                artifact_path_dir=test_yaml['artifact_path_dir'],
                                artifact=contract['contract']['artifact'],
                                links=None
                            ))
                            continue
                    else:
                        cobraPrint("[ERROR] CobraNotFound: Can't find artifact in contract.", "error", bold=True)
                        sys.exit()
            else:
                cobraPrint(
                    "[ERROR] CobraNotFound: Can't find contracts in test", "error", bold=True)
                sys.exit()
        else:
            cobraPrint(
                "[ERROR] CobraNotFound: Can't find artifact_path_dir in test", "error", bold=True)
            sys.exit()

        return tests

    def account(self, account_yaml):
        if 'address' in account_yaml:
            if 'gas' in account_yaml:
                if 'gas_price' in account_yaml:
                    return dict(account=dict(
                        address=account_yaml['address'],
                        gas=account_yaml['gas'],
                        gas_price=account_yaml['gas_price']
                    ))
                else:
                    return dict(account=dict(
                        address=account_yaml['address'],
                        gas=account_yaml['gas']
                    ))
            else:
                if 'gas_price' in account_yaml:
                    return dict(account=dict(
                        address=account_yaml['address'],
                        gas_price=account_yaml['gas_price']
                    ))
                else:
                    return dict(account=dict(
                        address=account_yaml['address']
                    ))
        elif 'gas' in account_yaml:
            if 'gas_price' in account_yaml:
                return dict(account=dict(
                    gas=account_yaml['gas'],
                    gas_price=account_yaml['gas_price']
                ))
            else:
                return dict(account=dict(
                    gas=account_yaml['gas']
                ))
        else:
            cobraPrint("[ERROR] CobraNotFound: Can address/gas in account.", "error", bold=True)
            sys.exit()

    def hdwallet(self, hdwallet_yaml):
        if 'mnemonic' in hdwallet_yaml or \
                'seed' in hdwallet_yaml or \
                'private' in hdwallet_yaml:
            # returns Mnemonic and Password
            if 'mnemonic' in hdwallet_yaml and 'password' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            password=hdwallet_yaml['password'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            password=hdwallet_yaml['password'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            password=hdwallet_yaml['password'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            password=hdwallet_yaml['password']
                        ))
            # returns Mnemonic
            elif 'mnemonic' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic']
                        ))
            # returns Mnemonic (Seed is alias Mnemonic) and Password
            if 'seed' in hdwallet_yaml and 'password' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            password=hdwallet_yaml['password'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            password=hdwallet_yaml['password'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            password=hdwallet_yaml['password'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            password=hdwallet_yaml['password']
                        ))
            # returns Mnemonic (Seed is alias Mnemonic)
            elif 'seed' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed']
                        ))
            # returns Private Key
            if 'private' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            private=hdwallet_yaml['private'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            private=hdwallet_yaml['private'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            private=hdwallet_yaml['private'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            private=hdwallet_yaml['private']
                        ))
        else:
            cobraPrint("[ERROR] CobraNotFound: Can't find mnemonic(seed)/private in hdwallet.", "error",
                       bold=True)
            sys.exit()

    def network(self, network_yaml):
        if 'development' in network_yaml:
            if 'host' in network_yaml['development'] or \
                    'url' in network_yaml['development']:
                if 'host' in network_yaml['development']:
                    if 'port' in network_yaml['development']:
                        # Protocol
                        if 'protocol' in network_yaml['development']:

                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                        # No Protocol
                        else:
                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port']
                                )
                    else:
                        cobraPrint("[ERROR] CobraNotFound: Can't find port in %s when you are using host."
                                   % 'development', "error", bold=True)
                        sys.exit()
                elif 'url' in network_yaml['development']:
                    # Port
                    if 'port' in network_yaml['development']:
                        # Protocol
                        if 'protocol' in network_yaml['development']:

                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                        # No Protocol
                        else:
                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port']
                                )
                    # No Port
                    else:
                        # Protocol
                        if 'protocol' in network_yaml['development']:

                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    url=network_yaml['development']['url'],
                                    protocol=network_yaml['development']['protocol']
                                )
                        # No Protocol
                        else:
                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    url=network_yaml['development']['url']
                                )
            else:
                cobraPrint("[ERROR] CobraNotFound: Can't find host/url in %s." % 'development',
                           "error", bold=True)
                sys.exit()
        else:
            cobraPrint("[ERROR] CobraNotFound: Can't find development in network.", "error", bold=True)
            sys.exit()


class Compile:
    
    import json
    from datetime import datetime

    network = """{,\n "networks": {},\n "updatedAt": "%s"\n}""" % str(datetime.now())

    def __init__(self):
        pass

    def strip(self, strip):
        return strip.strip()[1:-1]

    def bytecodeLinkToMD5(self, bytecode, contract_interface):
        count = 0
        contract_bytecode = []
        split_bytecode = re.split('__+', bytecode)
        files = self.bytecodeLinkFromFile(contract_interface)
        for index, contract in enumerate(split_bytecode):
            if len(contract) < 40 and (index % 2) != 0:
                underscore = "_"
                link_bytecode = 40
                file = "__" + str(files[count])
                length_of_file = len(file)
                contract_name = file + ((link_bytecode - length_of_file) * underscore)
                contract_bytecode.append(contract_name)
                count = count + 1
            else:
                contract_bytecode.append(contract)
        return "".join(contract_bytecode)

    def bytecodeLinkFromFile(self, contract_interface):
        files = []
        children = contract_interface['ast']['children']
        for attributes in children:
            try:
                file = attributes['attributes']['file']
                files.append(basename(file)[:-4])
            except KeyError:
                continue
        return files

    def isCompiled(self, file_path, contract_interface):
        try:
            with open(file_path, 'r') as read_file:
                return_file = read_file.read()
                contract_interface_file = jsonLoader(return_file,)
                try:
                    contract_interface_file = loads(return_file)['bin']
                except json.decoder.JSONDecodeError:
                    return False
                contract_interface_compiled = loads(contract_interface)['bin']
                if contract_interface_compiled == contract_interface_file:
                    read_file.close()
                    return True
                read_file.close()
        except KeyError:
            return False
        except FileNotFoundError:
            return False
        return False

    def toCompile(self, file_path_sol, allow_paths=None, import_remappings=None, more=None):
        try:
            import solc
            from solc import compile_source
        except ImportError:
            cobraPrint("Please install solc!", "error")
            sys.exit()
        if allow_paths is None:
            allow_paths = str(os.getcwd())

        if import_remappings is None:
            import_remappings = []

        if more is not None:
            more = True
        else:
            more = False

        solidity_contract = fileReader(file_path_sol)
        try:
            compiled_sol = compile_source(solidity_contract,
                                          allow_paths=allow_paths,
                                          import_remappings=import_remappings)
        except solc.exceptions.SolcError as solcError:
            solcError = str(solcError)
            solcErrorSplit = solcError.split('\n')
            if not more:
                cobraPrint("[ERROR] CobraCompileError: %s" % solcErrorSplit[0], "error", bold=True)
            else:
                cobraPrint("[ERROR] CobraCompileError: %s" % solcError, "error", bold=True)
            sys.exit()
        contract_interface = compiled_sol['<stdin>:' + basename(file_path_sol)[:-4]]
        contract_interface['bin'] = self.bytecode_link_to_md5(contract_interface['bin'], contract_interface)
        contract_interface['bin-runtime'] = self.bytecode_link_to_md5(
            contract_interface['bin-runtime'], contract_interface)
        contractName = """{\n "contractName": "%s",}""" % basename(file_path_sol)[:-4]
        artifact = web3.Web3().toText(dumps(contract_interface, indent=1).encode())
        artifact_contract_interface = "{%s}" % (self.strip(contractName) +
                                                self.strip(artifact)[:-1] +
                                                self.strip(self.network))
        return artifact_contract_interface
