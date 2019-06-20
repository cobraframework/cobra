from cobra import *


def _unittest(more=False):
    """
    Start testing Cobra using Unittest to test Smart Contract (Solidity file)

    The unittest unit testing framework was originally inspired by JUnit and has
    a similar flavor as major unit testing frameworks in other languages. It supports
    test automation, sharing of setup and shutdown code for tests, aggregation of
    tests into collections, and independence of the tests from the reporting framework.
    :return:
    """

    # Collection of test cases
    test_suite = TestSuite()
    test_case_classes = []

    # Initializing ethereum tester
    _ethereumTester = EthereumTester()
    # Initializing ethereum tester provider
    _ethereumTesterProvider = EthereumTesterProvider(_ethereumTester)
    # Initializing web3 added ethereum tester provider
    _web3 = Web3(_ethereumTesterProvider)

    def zero_gas_price_strategy(web3, transaction_params=None):
        # zero gas price makes testing simpler.
        return 0

    # Set gas price strategy
    _web3.eth.setGasPriceStrategy(zero_gas_price_strategy)
    # Initializing cobra interfaces
    interfaces = Interfaces(_web3, "./cobra.yaml", more)

    class CollectionInterfaces:
        web3 = _web3
        ethereum_tester = _ethereumTester
        compiled_interfaces = interfaces.get_interfaces()

    read_yaml = file_reader("./cobra.yaml")
    load_yaml = yaml_loader(read_yaml)
    if 'test' in load_yaml:
        test_yaml = load_yaml['test']
        if 'test_paths' in test_yaml:
            test_paths = test_yaml['test_paths']
            for test_path in test_paths:

                try:
                    test_loader = unittest.defaultTestLoader.discover(
                        start_dir=str(Path(test_path).resolve()), pattern='*_test.py',
                        top_level_dir=str(Path(test_path).resolve()))
                except ImportError as importError:
                    console_log(str(importError), "error", "ImportError")
                    sys.exit()

                for all_test_suite in test_loader:
                    for _test_suites in all_test_suite:
                        for _test_suite in _test_suites:
                            test_case_classes\
                                .append(_test_suite.__class__)

            # Added test case class on test suite array
            for test_case_class in list(set(test_case_classes)):
                test_suite.addTest(Test.cobra(test_case_class,
                                              collection_interfaces=CollectionInterfaces()))
            # Run Unittest
            unittest.TextTestRunner(verbosity=2).run(test_suite)

        else:
            console_log("test_paths in test", "error", "NotFound")
            sys.exit()

    else:
        console_log("test in cobra.yaml", "error", "NotFound")
        sys.exit()
