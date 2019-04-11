from eth_tester.exceptions import TransactionFailed
from test.contract import CobraFactory
from eth_tester import EthereumTester
from json import loads
import unittest
import sys
from configuration import CobraConfiguration
from solc import link_code
from os.path import join
from web3 import Web3


class CobraAccount(str):

    def __new__(cls, web3: Web3, address):
        obj = super().__new__(cls, address)
        obj.web3 = web3
        obj.address = address
        return obj

    # Send Ether
    def transfer(self, address, amount):
        self.web3.eth.sendTransaction({'to': address, 'from': self.address, 'value': amount})

    @property
    def balance(self):
        return self.web3.eth.getBalance(self.address)


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


class CobraTest(unittest.TestCase):

    def __init__(self, methodName='runTest', collectionInterfaces=None):
        super(CobraTest, self).__init__(methodName)
        if collectionInterfaces is None:
            collectionInterfaces = dict()
        try:
            self.cobra = CobraTester(
                collectionInterfaces.web3,
                collectionInterfaces.ethereumTester,
                collectionInterfaces.compiledInterfaces)
        except AttributeError:
            self.cobra = None

    @staticmethod
    def cobra(testCase_Class, collectionInterfaces=None):
        testLoader = unittest.TestLoader()
        testNames = testLoader.getTestCaseNames(testCase_Class)
        suite = unittest.TestSuite()
        for testName in testNames:
            suite.addTest(testCase_Class(testName, collectionInterfaces=collectionInterfaces))

        return suite


class CobraTester:

    def __init__(self, web3: Web3,
                 ethereumTester: EthereumTester,
                 compiledInterfaces=None):
        if compiledInterfaces is None:
            compiledInterfaces = dict()
        self.ethereumTester = ethereumTester
        self.web3 = web3

        self.compiledInterfaces = compiledInterfaces

    def contract(self, name):
        for compiledInterface in self.compiledInterfaces.keys():
            contractName = compiledInterface.split(":")
            if contractName[0] == name:
                interface = self.compiledInterfaces.get(compiledInterface)
                return self.new(interface)
            else:
                continue

    def new(self, interface):
        if isinstance(interface['abi'], str):
            interface['abi'] = loads(interface['abi'])
        return CobraFactory(self.web3, interface)

    @property
    def accounts(self):
        return [CobraAccount(self.web3, address)
                for address in self.ethereumTester.get_accounts()]

    @property
    def eth(self):
        # Return the w3 eth API
        return self.web3.eth

    @property
    def tx_fails(self):
        return CobraFailureHandler(self.ethereumTester)

    def now(self):
        #  Get this from the Ethereum block timestamp
        return self.web3.eth.getBlock('pending')['timestamp']

    def mine_blocks(self, number=1):
        self.ethereumTester.mine_blocks(number)


class CobraFailureHandler:

    def __init__(self, ethTester):
        self.ethTester = ethTester

    def __enter__(self):
        self.snapshotId = self.ethTester.take_snapshot()
        return self.snapshotId

    def __exit__(self, *args):
        assert len(args) > 0 and \
               args[0] is TransactionFailed, "Didn't revert transaction."
        self.ethTester.revert_to_snapshot(self.snapshotId)
        return True
