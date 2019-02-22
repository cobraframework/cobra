from web3 import Web3


class CobraAccount(str):
    def __new__(cls, web3: Web3, address):
        obj = super().__new__(cls, address)
        obj._web3 = web3
        obj._address = address
        return obj

    # Send Ether
    def transfer(self, address, amount):
        self._web3.eth.sendTransaction({'to': address, 'from': self._address, 'value': amount})

    @property
    def balance(self):
        return self._web3.eth.getBalance(self._address)