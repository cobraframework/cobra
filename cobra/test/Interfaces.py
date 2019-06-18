import sys
from solc import link_code
from os.path import join
from web3 import Web3

from cobra.project.configuration import Configuration
from cobra.utils import file_reader, yaml_loader, json_loader
from cobra.utils.console_log import console_log


class Interfaces(Configuration):

    def __init__(self, web3: Web3, yaml_file, more=False):
        super().__init__()
        self.web3 = web3
        self.contracts = dict()
        self.yaml_file = yaml_file
        self.more = more

    def get_interfaces(self):
        readied_yaml = file_reader(self.yaml_file)
        loaded_yaml = yaml_loader(readied_yaml)
        if 'test' in loaded_yaml:
            test_yaml = loaded_yaml['test']
            configurations_yaml = self.test(test_yaml)
            for configuration_yaml in configurations_yaml:
                artifact_json = join(configuration_yaml['artifact_path'],
                                     configuration_yaml['artifact'])
                readied_artifact_json = file_reader(artifact_json)
                loaded_artifact_json = json_loader(readied_artifact_json)
                if configuration_yaml['links'] is None:
                    self.test_with_out_link(loaded_artifact_json)
                else:
                    self.test_with_link(loaded_artifact_json, configuration_yaml['links'])
            return self.contracts
        else:
            console_log("test in cobra.yaml", "error", "NotFound")
            sys.exit()

    def get_links_address(self, links):
        contract_name_and_address = dict()
        for link in links:
            for contract in self.contracts.keys():
                contract = contract.split(":")
                if contract[0] == link[:-5]:
                    contract_name_and_address.setdefault(link[:-5], contract[1])
                elif contract[0] == link:
                    contract_name_and_address.setdefault(link, contract[1])
                else:
                    continue
        return contract_name_and_address

    def test_with_link(self, artifact, links):
        unlinked_bytecode = artifact['bin']
        get_link_address = self.get_links_address(links)
        linked_bytecode = link_code(unlinked_bytecode, get_link_address)

        try:
            contract_factory = self.web3.eth.contract(abi=artifact['abi'], bytecode=linked_bytecode)
        except ValueError as valueError:
            value_error = str(valueError.args.__getitem__(0))
            if "'" in value_error and not self.more:
                error = str(value_error).split("'")
                console_log(str(error[0]), "error", "ValueError")
            elif "'" in value_error and self.more:
                console_log(
                    str(value_error), "error", "ValueError")
            elif not self.more:
                console_log(
                    str(value_error).strip('\n')[0], "error", "ValueError")
            elif self.more:
                console_log(
                    str(value_error), "error", "ValueError")
            sys.exit()

        # Get transaction hash
        tx_hash = contract_factory.constructor().transact()

        address = self.web3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        contract = {"abi": artifact['abi'], "bytecode": linked_bytecode}
        contract_name_and_address = artifact['contractName'] + ":" + str(address)
        self.contracts.setdefault(contract_name_and_address, contract)

    def test_with_out_link(self, artifact):
        try:
            contract_factory = self.web3.eth.contract(abi=artifact['abi'],
                                                      bytecode=artifact['bin'])
        except ValueError as valueError:
            value_error = str(valueError.args.__getitem__(0))
            if "'" in value_error and not self.more:
                error = str(value_error).split("'")
                console_log(str(error[0]), "error", "ValueError")
            elif "'" in value_error and self.more:
                console_log(
                    str(value_error), "error", "ValueError")
            elif not self.more:
                console_log(
                    str(value_error).strip('\n')[0], "error", "ValueError")
            elif self.more:
                console_log(
                    str(value_error), "error", "ValueError")
            sys.exit()

        # Get transaction hash
        tx_hash = contract_factory.constructor().transact()

        address = self.web3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        contract = {"abi": artifact['abi'], "bytecode": artifact['bin']}
        contract_name_and_address = artifact['contractName'] + ":" + str(address)
        self.contracts.setdefault(contract_name_and_address, contract)
