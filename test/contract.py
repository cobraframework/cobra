from eth_utils import event_abi_to_log_topic
from web3.utils.events import get_event_data
from functools import partial as partial_fn
from web3.contract import ImplicitContract
from test.log import CobraLog
from web3 import Web3


class CobraInstance:
    """Deployed instance of a contract"""

    def __init__(self, _web3: Web3, address, interface):
        self.web3 = _web3
        self.__address = address
        self.__instance = ImplicitContract(self.web3.eth.contract(self.__address, **interface))
        # Register new filter to watch for logs from this instance's address
        self.__filter = self.web3.eth.filter({
            # Include events from the deployment stage
            'fromBlock': self.web3.eth.blockNumber - 1,
            'address': self.__address
        })
        self.__event_signatures = self.get_event_signatures(interface['abi'])
        self.__event_processors = self.get_event_processors(interface['abi'])

    def __getattr__(self, name):
        """Delegates to either specialized methods or instance ABI"""
        if name in dir(self):
            # Specialized testing methods
            return getattr(self, name)
        elif name in self._events:
            return self._gen_log(name)
        else:
            # Method call of contract instance
            return getattr(self.__instance, name)

    @property
    def _events(self):
        return self.__event_signatures.keys()

    def _gen_log(self, name):
        return lambda v: CobraLog(name, v)

    @property
    def address(self):
        """This contract's address"""
        return self.__address

    @property
    def balance(self):
        """Ether balance of this contract (in wei)"""
        return self.web3.eth.getBalance(self.__address)

    @property
    def codesize(self):
        """Codesize of this contract (in bytes)"""
        return len(self.web3.eth.getCode(self.__address)[2:]) / 2

    @property
    def hascode(self):
        """Check if this contract currently has code (usually indicating suicide)"""
        return self.codesize != 0

    def process_logs(self, logs):
        processed_logs = []
        for log in logs:
            log_signature = log['topics'][0]
            if log_signature in self.__event_processors.keys():
                p_log = self.__event_processors[log_signature](log)
                processed_logs.append(CobraLog(p_log['event'], p_log['args']))
        return processed_logs

    @property
    def logs(self):
        """Returns all the event logs ever added for this contract"""
        return self.process_logs(self.__filter.get_all_entries())

    def get_event_signatures(self, abi_list):
        signatures = dict()
        for abi in abi_list:
            if abi['type'] == 'event':
                signatures[abi['name']] = event_abi_to_log_topic(abi)
        return signatures

    def get_event_processors(self, abi_list):
        processors = dict()
        for abi in abi_list:
            if abi['type'] == 'event':
                processors[event_abi_to_log_topic(abi)] = partial_fn(get_event_data, abi)
        return processors


class CobraFactory:
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
        return CobraInstance(self.web3, address, self.interface)

    def __getattr__(self, name):
        return getattr(self.contract_factory, name)

    def clean_modifiers(self, modifiers):
        cleaned_modifiers = modifiers.copy()
        for name, modifier in modifiers.items():
            for key, value in modifier.items():
                if not isinstance(value, str) or not isinstance(value, int):
                    cleaned_modifiers[name][key] = str(value)
        return cleaned_modifiers
