from web3 import Web3
from .instance import Instance


class Factory:
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
        return Instance(self.web3, address, self.interface)

    def __getattr__(self, name):
        return getattr(self.contract_factory, name)

    @staticmethod
    def clean_modifiers(modifiers):
        cleaned_modifiers = modifiers.copy()
        for name, modifier in modifiers.items():
            for key, value in modifier.items():
                if not isinstance(value, str) or not isinstance(value, int):
                    cleaned_modifiers[name][key] = str(value)
        return cleaned_modifiers
