from web3 import Web3


class Account(str):

    def __new__(cls, web3: Web3, address):
        obj = super().__new__(cls, address)
        obj.web3 = web3
        obj.address = address
        return obj

    # Send Ether
    def transfer(self, address, amount):
        self.web3.eth.sendTransaction({
            'to': address,
            'from': self.address,
            'value': amount
        })

    @property
    def balance(self):
        return self.web3.eth.getBalance(self.address)
