import unittest

from .account import Account
from .log import Log
from .factory import Factory
from .failure_handler import FailureHandler
from .tester import Tester


class Test(unittest.TestCase):

    def __init__(self, method_name='runTest', collection_interfaces=None):
        super(Test, self).__init__(method_name)
        if collection_interfaces is None:
            collection_interfaces = dict()
        try:
            self.cobra = Tester(
                _web3=collection_interfaces.web3,
                ethereum_tester=collection_interfaces.ethereum_tester,
                compiled_interfaces=collection_interfaces.compiled_interfaces)
        except AttributeError:
            self.cobra = None

    @staticmethod
    def cobra(test_case_class, collection_interfaces=None):
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(test_case_class)
        suite = unittest.TestSuite()
        for test_name in test_names:
            suite.addTest(test_case_class(test_name, collection_interfaces=collection_interfaces))

        return suite
