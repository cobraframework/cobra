from eth_tester.exceptions import TransactionFailed
from test.contract import CobraFactory
from eth_tester import EthereumTester
from json import loads
from web3 import Web3
import unittest


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
