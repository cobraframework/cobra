from eth_tester.exceptions import TransactionFailed
from eth_tester import EthereumTester


class CobraFailureHandler:

    def __init__(self, ethereum_tester: EthereumTester):
        self.ethereum_tester = ethereum_tester

    def __enter__(self):
        self.snapshotId = self.ethereum_tester.take_snapshot()
        return self.snapshotId

    def __exit__(self, *args):
        assert len(args) > 0 and \
               args[0] is TransactionFailed, "Didn't revert transaction."
        self.ethereum_tester.revert_to_snapshot(self.snapshotId)
        return True
