from configuration import CobraConfiguration
from solc import link_code
from os.path import join
from web3 import Web3
import sys


class CobraInterfaces(CobraConfiguration):

    def __init__(self, web3: Web3, yamlFile, more=None):
        super().__init__()
        self.web3 = web3
        self.contracts = dict()
        self.yamlFile = yamlFile
        if more is not None:
            self.more = True
        else:
            self.more = False

    def getInterfaces(self):
        readiedYaml = self.file_reader(self.yamlFile)
        loadedYaml = self.yaml_loader(readiedYaml)
        if 'test' in loadedYaml:
            testYaml = loadedYaml['test']
            configurationsYaml = self.test(testYaml)
            for configurationYaml in configurationsYaml:
                artifactJson = join(configurationYaml['artifact_path_dir'],
                                    configurationYaml['artifact'])
                readiedArtifactJson = self.file_reader(artifactJson)
                loadedArtifactJson = self.json_loader(readiedArtifactJson)
                if configurationYaml['links'] is None:
                    self.testWithOutLink(loadedArtifactJson)
                else:
                    self.testWithLink(loadedArtifactJson, configurationYaml['links'])
            return self.contracts
        else:
            self.cobra_print(
                "[ERROR] CobraNotFound: Can't find test in cobra.yaml", "error", bold=True)
            sys.exit()

    def getLinksAddress(self, links):
        contractNameAndAddress = dict()
        for link in links:
            for contract in self.contracts.keys():
                contract = contract.split(":")
                if contract[0] == link[:-5]:
                    contractNameAndAddress.setdefault(link[:-5], contract[1])
                elif contract[0] == link:
                    contractNameAndAddress.setdefault(link, contract[1])
                else:
                    continue
        return contractNameAndAddress

    def testWithLink(self, artifact, links):
        unlinkedBytecode = artifact['bin']
        getLinkAddress = self.getLinksAddress(links)
        linkedBytecode = link_code(unlinkedBytecode, getLinkAddress)

        try:
            contractFactory = self.web3.eth.contract(abi=artifact['abi'], bytecode=linkedBytecode)
        except ValueError as valueError:
            valueError = str(valueError.args.__getitem__(0))
            if "'" in valueError and not self.more:
                error = str(valueError).split("'")
                self.cobra_print(
                    "[ERROR] CobraValueError: %s" % error[0], "error", bold=True)
            elif "'" in valueError and self.more:
                self.cobra_print(
                    "[ERROR] CobraValueError: %s" % valueError, "error", bold=True)
            elif not self.more:
                self.cobra_print(
                    "[ERROR] CobraValueError: %s" % valueError[:100], "error", bold=True)
            elif self.more:
                self.cobra_print(
                    "[ERROR] CobraValueError: %s" % valueError, "error", bold=True)
            sys.exit()

        # Get transaction hash
        txHash = contractFactory.constructor().transact()

        address = self.web3.eth.getTransactionReceipt(txHash)['contractAddress']
        contract = {"abi": artifact['abi'], "bytecode": linkedBytecode}
        contractNameAndAddress = artifact['contractName'] + ":" + str(address)
        self.contracts.setdefault(contractNameAndAddress, contract)

    def testWithOutLink(self, artifact):
        try:
            contractFactory = self.web3.eth.contract(abi=artifact['abi'], bytecode=artifact['bin'])
        except ValueError as valueError:
            valueError = str(valueError.args.__getitem__(0))
            if "'" in valueError and not self.more:
                error = str(valueError).split("'")
                self.cobra_print(
                    "[ERROR] CobraValueError: %s" % error[0], "error", bold=True)
            elif "'" in valueError and self.more:
                self.cobra_print(
                    "[ERROR] CobraValueError: %s" % valueError, "error", bold=True)
            elif not self.more:
                self.cobra_print(
                    "[ERROR] CobraValueError: %s..." % valueError[:75], "error", bold=True)
            elif self.more:
                self.cobra_print(
                    "[ERROR] CobraValueError: %s" % valueError, "error", bold=True)
            sys.exit()

        # Get transaction hash
        txHash = contractFactory.constructor().transact()

        address = self.web3.eth.getTransactionReceipt(txHash)['contractAddress']
        contract = {"abi": artifact['abi'], "bytecode": artifact['bin']}
        contractNameAndAddress = artifact['contractName'] + ":" + str(address)
        self.contracts.setdefault(contractNameAndAddress, contract)
