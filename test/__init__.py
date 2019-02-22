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



