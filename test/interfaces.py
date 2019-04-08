from configuration import CobraConfiguration
from solc import link_code
from os.path import join
from web3 import Web3
import sys


class CobraInterfaces(CobraConfiguration):

    def __init__(self, _web3: Web3, yaml_file):
        super().__init__()
        self.web3 = _web3
        self.contracts = dict()
        self.yaml_file = yaml_file






