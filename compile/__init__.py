from json import loads, dumps
import json
from os.path import basename
import solc
import sys
from solc import compile_source
from datetime import datetime
import web3
from lazyme.string import color_print
import re
import os


class CobraCompile:

    network = """{,\n "networks": {},\n "updatedAt": "%s"\n}""" % str(datetime.now())

    def __init__(self):
        pass

    def cobra_print(self, text, color=None, bold=False, background=None, underline=False):
        if color == 'success':
            return color_print(text, color='green', bold=bold, highlighter=background, underline=underline)
        elif color == 'warning':
            return color_print(text, color='yellow', bold=bold, highlighter=background, underline=underline)
        elif color == 'error':
            return color_print(text, color='red', bold=bold, highlighter=background, underline=underline)
        else:
            return color_print(text, bold=bold, highlighter=background, underline=underline)

    def strip(self, strip):
        return strip.strip()[1:-1]

    def file_reader(self, file_path):
        try:
            with open(file_path, 'r') as read_file:
                return_file = read_file.read()
                read_file.close()
                return return_file
        except FileNotFoundError:
            self.cobra_print("[ERROR] CobraFileNotFound: %s" % file_path, "error", bold=True)
            sys.exit()

    def file_writer(self, file_path, docs):
        with open(file_path, 'w') as write_file:
            write_file.write(docs)
            write_file.close()
            return

    def bytecode_link_to_md5(self, bytecode, contract_interface):
        count = 0
        contract_bytecode = []
        split_bytecode = re.split('__+', bytecode)
        files = self.bytecode_link_from_file(contract_interface)
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

    def bytecode_link_from_file(self, contract_interface):
        files = []
        children = contract_interface['ast']['children']
        for attributes in children:
            try:
                file = attributes['attributes']['file']
                files.append(basename(file)[:-4])
            except KeyError:
                continue
        return files

    def is_compiled(self, file_path, contract_interface):
        try:
            with open(file_path, 'r') as read_file:
                return_file = read_file.read()
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

    def to_compile(self, file_path_sol, allow_paths=None, import_remappings=None, more=None):
        if allow_paths is None:
            allow_paths = str(os.getcwd())

        if import_remappings is None:
            import_remappings = []

        if more is not None:
            more = True
        else:
            more = False

        solidity_contract = self.file_reader(file_path_sol)
        try:
            compiled_sol = compile_source(solidity_contract, allow_paths=allow_paths, import_remappings=import_remappings)
        except solc.exceptions.SolcError as solcError:
            solcError = str(solcError)
            solcErrorSplit = solcError.split('\n')
            if not more:
                self.cobra_print("[ERROR] CobraCompileError: %s" % solcErrorSplit[0], "error", bold=True)
            else:
                self.cobra_print("[ERROR] CobraCompileError: %s" % solcError, "error", bold=True)
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
