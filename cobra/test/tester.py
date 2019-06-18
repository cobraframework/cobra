from eth_tester import EthereumTester
from json import loads
from web3 import Web3

from .account import Account
from .factory import Factory
from .failure_handler import FailureHandler


class Tester:

    def __init__(self, _web3: Web3,
                 ethereum_tester: EthereumTester,
                 compiled_interfaces=None):
        if compiled_interfaces is None:
            compiled_interfaces = dict()
        self.ethereum_tester = ethereum_tester
        self.web3 = _web3

        self.compiled_interfaces = compiled_interfaces

    def contract(self, name):
        for compiledInterface in self.compiled_interfaces.keys():
            contract_name = compiledInterface.split(":")
            if contract_name[0] == name:
                interface = self.compiled_interfaces.get(compiledInterface)
                return self.new(interface)
            else:
                continue

    def new(self, interface):
        if isinstance(interface['abi'], str):
            interface['abi'] = loads(interface['abi'])
        return Factory(self.web3, interface)

    @property
    def accounts(self):
        return [Account(self.web3, address)
                for address in self.ethereum_tester.get_accounts()]

    @property
    def eth(self):
        # Return the w3 eth API
        return self.web3.eth

    @property
    def tx_fails(self):
        return FailureHandler(self.ethereum_tester)

    def now(self):
        #  Get this from the Ethereum block timestamp
        return self.web3.eth.getBlock('pending')['timestamp']

    def mine_blocks(self, number=1):
        self.ethereum_tester.mine_blocks(number)
