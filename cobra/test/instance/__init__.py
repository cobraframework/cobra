from web3.contract import ImplicitContract
from web3 import Web3
from cobra.test.log import Log
from .event import get_event_signatures, get_event_processors


class Instance:
    """Deployed instance of a contract"""

    def __init__(self, _web3: Web3, address, interface):
        self.web3 = _web3
        self.__address = address
        self.__instance = ImplicitContract(
            self.web3.eth.contract(self.__address, **interface))
        # Register new filter to watch for logs from this instance's address
        self.__filter = self.web3.eth.filter({
            # Include events from the deployment stage
            'fromBlock': self.web3.eth.blockNumber - 1,
            'address': self.__address
        })
        self.__event_signatures = get_event_signatures(interface['abi'])
        self.__event_processors = get_event_processors(interface['abi'])

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

    @staticmethod
    def _gen_log(name):
        return lambda v: Log(name, v)

    @property
    def address(self):
        """This contract's address"""
        return self.__address

    @property
    def balance(self):
        """Ether balance of this contract (in wei)"""
        return self.web3.eth.getBalance(self.__address)

    @property
    def code_size(self):
        """Codesize of this contract (in bytes)"""
        return len(self.web3.eth.getCode(self.__address)[2:]) / 2

    @property
    def has_code(self):
        """Check if this contract currently has code (usually indicating suicide)"""
        return self.code_size != 0

    def process_logs(self, logs):
        processed_logs = []
        for log in logs:
            log_signature = log['topics'][0]
            if log_signature in self.__event_processors.keys():
                p_log = self.__event_processors[log_signature](log)
                processed_logs.append(Log(p_log['event'], p_log['args']))
        return processed_logs

    @property
    def logs(self):
        """Returns all the event logs ever added for this contract"""
        return self.process_logs(self.__filter.get_all_entries())
