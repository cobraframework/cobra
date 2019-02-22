from eth_tester.exceptions import TransactionFailed
from test.contract import CobraFactory
from test.account import CobraAccount
from eth_tester import EthereumTester
from json import loads
from web3 import Web3
import unittest


class CobraTest(unittest.TestCase):

    def __init__(self, methodName='runTest', collectionInterfaces=None):
        super(CobraTest, self).__init__(methodName)
        if collectionInterfaces is None:
            collectionInterfaces = dict()
        try:
            self.cobra = CobraTester(
                collectionInterfaces._web3,
                collectionInterfaces._ethereum_tester,
                collectionInterfaces.compiled_interfaces)
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

    def __init__(self, _web3: Web3, _ethereum_tester: EthereumTester,
                 compiled_interfaces=None):
        if compiled_interfaces is None:
            compiled_interfaces = dict()
        self.ethereum_tester = _ethereum_tester
        self.web3 = _web3

        self.compiled_interfaces = compiled_interfaces

    def contract(self, name):
        for compiled_interface in self.compiled_interfaces.keys():
            contract_name = compiled_interface.split(":")
            if contract_name[0] == name:
                interface = self.compiled_interfaces.get(compiled_interface)
                return self.new(interface)
            else:
                continue

    def new(self, interface):
        if isinstance(interface['abi'], str):
            interface['abi'] = loads(interface['abi'])
        return CobraFactory(self.web3, interface)

    @property
    def accounts(self):
        return [CobraAccount(self.web3, a) for a in self.ethereum_tester.get_accounts()]

    @property
    def eth(self):
        # Return the w3 eth API
        return self.web3.eth

    @property
    def tx_fails(self):
        return CobraFailureHandler(self.ethereum_tester)

    def now(self):
        #  Get this from the Ethereum block timestamp
        return self.web3.eth.getBlock('pending')['timestamp']

    def mine_blocks(self, number=1):
        self.ethereum_tester.mine_blocks(number)

