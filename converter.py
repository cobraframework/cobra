from solc import compile_source
from json import dumps, loads
from os.path import basename
import json
import web3
import sys

UNDERSCORE = "_"
LINK_LENGTH = 36


class CobraCompiler:

    def __init__(self, compiled_contracts):
        super().__init__()
        self.contracts = dict()

        for compiled_contract in compiled_contracts.keys():
            contract_interface = compiled_contracts.get(compiled_contract)

            contract_link = self.links_absolute_path(contract_interface)
            if contract_link:
                contract_and_link = compiled_contract.split(":")[1] + ":" + str(":".join(
                    basename(link)[:-4] for link in contract_link))
            else:
                contract_and_link = compiled_contract.split(":")[1]

            links_from_file = self.links_from_file(contract_interface)
            if links_from_file is None:
                links_from_absolutes_file = self.links_from_absolutes_file(contract_interface)
                self.contracts[contract_and_link] = links_from_absolutes_file
            else:
                self.contracts[contract_and_link] = links_from_file

    def __call__(self, *args, **kwargs):
        return self.contracts

    def links_file_path(self, contract_interface):
        files = []
        children = contract_interface['ast']['children']
        for attributes in children:
            try:
                files.append(attributes['attributes']['file'])
            except KeyError:
                continue
        return files

    def file_writer(self, file_path, docs):
        with open(file_path, 'w') as write_file:
            write_file.write(docs)
            write_file.close()
            return

    def links_absolute_path(self, interface):
        absolutes = []
        children = interface['ast']['children']
        for attributes in children:
            try:
                absolutes.append(attributes['attributes']['absolutePath'])
            except KeyError:
                continue
        return absolutes

    def links_from_file(self, contract_interface):
        links_file = self.links_file_path(contract_interface)
        for link_file in links_file:

            contract_name = basename(link_file)[:-4]
            contract_name_len = len(contract_name)
            link_file = link_file + ":" + contract_name
            link_file_path = link_file[:36]

            bytecode = contract_interface['bin']
            bytecode_runtime = contract_interface['bin-runtime']

            if "__" + link_file_path + "__" in contract_interface['bin'] and \
                    "__" + link_file_path + "__" in contract_interface['bin-runtime']:
                underscore_in_links = LINK_LENGTH - len(link_file_path)
                link_file_name = contract_name + \
                                 (((LINK_LENGTH - contract_name_len) - underscore_in_links) * UNDERSCORE)

                contract_interface['bin'] = bytecode.replace(link_file_path, link_file_name, 1)
                contract_interface['bin-runtime'] = bytecode_runtime.replace(link_file_path, link_file_name, 1)
                continue
            elif "__" + link_file_path[2:] + "__" in contract_interface['bin'] and \
                    "__" + link_file_path[2:] + "__" in contract_interface['bin-runtime']:
                link_file_path = link_file_path[2:]
                underscore_in_links = LINK_LENGTH - len(link_file_path)
                link_file_name = contract_name + \
                                 (((LINK_LENGTH - contract_name_len) - underscore_in_links) * UNDERSCORE)

                contract_interface['bin'] = bytecode.replace(link_file_path, link_file_name, 1)
                contract_interface['bin-runtime'] = bytecode_runtime.replace(link_file_path, link_file_name, 1)
                continue
            else:
                return None
        return contract_interface

    def links_from_absolutes_file(self, contract_interface):
        links_absolutes = self.links_absolute_path(contract_interface)
        contract_interface_bin = contract_interface['bin']
        contract_interface_bin_runtime = contract_interface['bin-runtime']
        for links_absolute in links_absolutes:
            contract_name = basename(links_absolute)[:-4]
            contract_name_len = len(contract_name)
            links_absolute = links_absolute + ":" + contract_name
            links_absolute_path = links_absolute[:36]

            split_bytecode = contract_interface_bin.split(links_absolute_path, 1)
            split_bytecode_runtime = contract_interface_bin_runtime.split(links_absolute_path, 1)
            contract_bytecode = []
            contract_bytecode_runtime = []

            for index, contract in enumerate(split_bytecode):
                if len(contract) > LINK_LENGTH and (index % 2) != 0:
                    underscore_in_links = LINK_LENGTH - len(links_absolute_path)
                    link_absolute_name = contract_name + (
                            ((LINK_LENGTH - contract_name_len) - underscore_in_links) * UNDERSCORE)
                    contract_bytecode.append(link_absolute_name)
                contract_bytecode.append(contract)
            contract_interface_bin = "".join(contract_bytecode)

            for index, contract in enumerate(split_bytecode_runtime):
                if len(contract) > LINK_LENGTH and (index % 2) != 0:
                    underscore_in_links = LINK_LENGTH - len(links_absolute_path)
                    link_absolute_name = contract_name + (
                            ((LINK_LENGTH - contract_name_len) - underscore_in_links) * UNDERSCORE)
                    contract_bytecode_runtime.append(link_absolute_name)
                contract_bytecode_runtime.append(contract)
            contract_interface_bin_runtime = "".join(contract_bytecode_runtime)

        contract_interface['bin'] = contract_interface_bin
        contract_interface['bin-runtime'] = contract_interface_bin_runtime
        return contract_interface


print(CobraCompiler("/home/meheret/PycharmProjects/Cobra/MetaCoin.sol",
                    ["/home/meheret/PycharmProjects/Cobra/"])())
