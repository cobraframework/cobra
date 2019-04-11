from eth_tester.exceptions import TransactionFailed
from eth_tester import EthereumTester
from json import loads
import unittest
import sys
from collections import Mapping
from configuration import CobraConfiguration
from solc import link_code
from os.path import join
from eth_utils import event_abi_to_log_topic
from web3.utils.events import get_event_data
from functools import partial as partial_fn
from web3.contract import ImplicitContract
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


class CobraLog(Mapping):

    def __new__(cls, event, args):
        obj = super().__new__(cls)
        obj._event = event
        obj._args = args
        return obj

    def __eq__(self, other):
        if not isinstance(other, CobraLog):
            return False
        if self._event != other._event:
            return False
        return self._args == other._args

    def __iter__(self):
        return iter(self._args)

    def __len__(self):
        return len(self._args)

    def __getitem__(self, key):
        return self._args[key]


class CobraInstance:
    """Deployed instance of a contract"""

    def __init__(self, _web3: Web3, address, interface):
        self.web3 = _web3
        self.__address = address
        self.__instance = ImplicitContract(self.web3.eth.contract(self.__address, **interface))
        # Register new filter to watch for logs from this instance's address
        self.__filter = self.web3.eth.filter({
            # Include events from the deployment stage
            'fromBlock': self.web3.eth.blockNumber - 1,
            'address': self.__address
        })
        self.__event_signatures = self.get_event_signatures(interface['abi'])
        self.__event_processors = self.get_event_processors(interface['abi'])

    def __getattr__(self, name):
        """Delegates to either specialized methods or instance ABI"""
        if name in dir(self):
            # Specialized testing methods
            return getattr(self, name)
        elif name in self._events:
            return self._gen_log(name)
        else:
            # Method call of contract instance
            return getattr(self.__instance, name)

    @property
    def _events(self):
        return self.__event_signatures.keys()

    def _gen_log(self, name):
        return lambda v: CobraLog(name, v)

    @property
    def address(self):
        """This contract's address"""
        return self.__address

    @property
    def balance(self):
        """Ether balance of this contract (in wei)"""
        return self.web3.eth.getBalance(self.__address)

    @property
    def codesize(self):
        """Codesize of this contract (in bytes)"""
        return len(self.web3.eth.getCode(self.__address)[2:]) / 2

    @property
    def hascode(self):
        """Check if this contract currently has code (usually indicating suicide)"""
        return self.codesize != 0

    def process_logs(self, logs):
        processed_logs = []
        for log in logs:
            log_signature = log['topics'][0]
            if log_signature in self.__event_processors.keys():
                p_log = self.__event_processors[log_signature](log)
                processed_logs.append(CobraLog(p_log['event'], p_log['args']))
        return processed_logs

    @property
    def logs(self):
        """Returns all the event logs ever added for this contract"""
        return self.process_logs(self.__filter.get_all_entries())

    def get_event_signatures(self, abi_list):
        signatures = dict()
        for abi in abi_list:
            if abi['type'] == 'event':
                signatures[abi['name']] = event_abi_to_log_topic(abi)
        return signatures

    def get_event_processors(self, abi_list):
        processors = dict()
        for abi in abi_list:
            if abi['type'] == 'event':
                processors[event_abi_to_log_topic(abi)] = partial_fn(get_event_data, abi)
        return processors


class CobraFactory:
    """Factory (prototype) of a contract"""

    def __init__(self, _web3: Web3, interface):
        self.web3 = _web3
        self.interface = interface
        self.contract_factory = self.web3.eth.contract(**self.interface)

    def deploy(self, *args, **kwargs):
        """Deploy a new instance of this contract"""
        kwargs = self.clean_modifiers(kwargs)
        if 'transact' in kwargs.keys():
            kwargs['transaction'] = kwargs['transact']
            del kwargs['transact']

        tx_hash = self.contract_factory.constructor(*args).transact(**kwargs)
        address = self.web3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return CobraInstance(self.web3, address, self.interface)

    def __getattr__(self, name):
        return getattr(self.contract_factory, name)

    def clean_modifiers(self, modifiers):
        cleaned_modifiers = modifiers.copy()
        for name, modifier in modifiers.items():
            for key, value in modifier.items():
                if not isinstance(value, str) or not isinstance(value, int):
                    cleaned_modifiers[name][key] = str(value)
        return cleaned_modifiers


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
            contractFactory = self.web3.eth.contract(abi=artifact['abi'],
                                                     bytecode=artifact['bin'])
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
