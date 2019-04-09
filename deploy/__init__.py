from lazyme.string import color_print
from json import loads, dumps
import json
from solc import link_code
from provider import CobraProvider
import requests
import random
from os.path import join
import sys
import websockets
from datetime import datetime

ACCOUNT_TEXT = """
Deploying to:
    Address: %s
"""
HDWALLET_TEXT = """Deploying to:
    Address: %s
    Public Key: %s
    Private Key: %s"""


class CobraDeploy(CobraProvider):
    network = """{,
     "network": {},
     "updatedAt": "%s"
    }""" % str(datetime.now())

    def __init__(self, cobraNetwork):
        self.cobraNetwork = cobraNetwork
        self.web3 = self.get_web3()
        self.account = self.get_account()
        self.hdwallet = self.get_hdwallet()
        self.display_account()

    def cobra_print(self, text, color=None, bold=False, background=None, underline=False):
        if color == 'success':
            return color_print(text, color='green', bold=bold, highlighter=background, underline=underline)
        elif color == 'warning':
            return color_print(text, color='yellow', bold=bold, highlighter=background, underline=underline)
        elif color == 'error':
            return color_print(text, color='red', bold=bold, highlighter=background, underline=underline)
        else:
            return color_print(text, bold=bold, highlighter=background, underline=underline)

    def display_account(self):
        if self.account is not None:
            self.cobra_print(ACCOUNT_TEXT % self.web3.toChecksumAddress(self.account['address']), bold=True)
        if self.hdwallet is not None:
            self.cobra_print(HDWALLET_TEXT % (self.web3.toChecksumAddress(self.hdwallet['address']),
                                              self.hdwallet['public_key'],
                                              self.hdwallet['private_key']), bold=True)

        else:
            self.cobra_print(ACCOUNT_TEXT % self.web3.eth.accounts[0], bold=True)

    def file_reader(self, file_path):
        try:
            with open(file_path, 'r') as read_file:
                return_file = read_file.read()
                read_file.close()
                return return_file
        except FileNotFoundError:
            self.cobra_print("FileNotFound: %s" % file_path, "error", bold=True)
            sys.exit()

    def file_writer(self, file_path, docs):
        with open(file_path, 'w') as write_file:
            write_file.write(docs)
            write_file.close()
            return

    def Strip(self, strip):
        return strip.strip()[1:-1]

    def generate_numbers(self, size=32):
        string = []
        for k in range(1, size + 1):
            string.append(random.choice('1029384756'))
        return "".join(string)

    def isDeployed(self, artifact):
        try:
            for network in artifact['networks'].keys():
                deployed = artifact['networks'].get(network)
                try:
                    deployedWeb3 = self.web3.eth.getTransactionReceipt(deployed['transactionHash'])
                    if deployed['contractAddress'] == deployedWeb3['contractAddress']:
                        return True
                    else:
                        continue
                except TypeError:
                    continue
                except requests.exceptions.ConnectionError:
                    self.cobra_print(
                        "[ERROR] HTTPConnectionPool: '%s' failed!" % (self.get_url_host_port()),
                        "error", bold=True)
                    sys.exit()
                except websockets.exceptions.InvalidMessage:
                    self.cobra_print(
                        "[ERROR] WebSocketsConnectionPool: '%s' failed!" % (self.get_url_host_port()),
                        "error", bold=True)
                    sys.exit()
                except FileNotFoundError:
                    self.cobra_print(
                        "[ERROR] ICPConnectionPool: '%s' failed!" % (self.get_url_host_port()),
                        "error", bold=True)
                    sys.exit()
        except KeyError:
            return False

    def get_links_address(self, dir_path, links):
        contract_name_and_address = {}
        for link in links:
            link_file_path = join(dir_path, link)
            artifact_not_loads = self.file_reader(link_file_path)
            try:
                artifact = loads(artifact_not_loads)
                try:
                    networks = artifact['networks']
                    for network in networks.keys():
                        deployed = networks.get(network)
                        try:
                            deployed_web3 = self.web3.eth.getTransactionReceipt(deployed['transactionHash'])
                            if deployed['contractAddress'] == deployed_web3['contractAddress']:
                                link_name = link[:-5]
                                contract_name_and_address.setdefault(link_name, deployed['contractAddress'])
                            else:
                                continue
                        except TypeError:
                            continue
                except KeyError:
                    return
            except json.decoder.JSONDecodeError:
                self.cobra_print("ArtifactDecodeError: %s" % link_file_path, "error", bold=True)
                return
        return contract_name_and_address

    def deploy_contract(self, contract):
        if self.account is not None:
            # self.web3.personal.importRawKey(
            #     self.account['private_key'], 'cobraframework')
            if 'gas' in self.account:
                transaction = {
                    'from': self.web3.toChecksumAddress(self.account['address']),
                    'gas': self.account['gas']
                }
                tx_hash = contract.deploy(transaction=transaction)
                return tx_hash
            else:
                transaction = {
                    'from': self.web3.toChecksumAddress(self.account['address']),
                    'gas': 3000000
                }
                tx_hash = contract.deploy(transaction=transaction)
                return tx_hash
        elif self.hdwallet is not None:
            # self.web3.personal.importRawKey(
            #     self.hdwallet['private_key'], 'cobraframework')
            if 'gas' in self.hdwallet:
                transaction = {
                    'from': self.web3.toChecksumAddress(self.hdwallet['address']),
                    'gas': self.hdwallet['gas']
                }
                tx_hash = contract.deploy(transaction=transaction)
                return tx_hash
            else:
                transaction = {
                    'from': self.web3.toChecksumAddress(self.hdwallet['address']),
                    'gas': 3000000
                }
                tx_hash = contract.deploy(transaction=transaction)
                return tx_hash
        else:
            transaction = {
                'from': self.web3.eth.accounts[0],
                'gas': 3000000
            }
            tx_hash = contract.deploy(transaction=transaction)
            return tx_hash

    def deploy_with_link(self, dir_path, contract, links):
        file_path = join(dir_path, contract)
        artifact_not_loads = self.file_reader(file_path)
        try:
            artifact = loads(artifact_not_loads)
        except json.decoder.JSONDecodeError:
            self.cobra_print("ArtifactDecodeError: %s" % file_path, "error", bold=True)
            return

        if not self.isDeployed(artifact):
            self.cobra_print("Deploying " + contract[:-5] + "...", "warning", bold=True)
            abi = artifact['abi']
            unlinked_bytecode = artifact['bin']
            get_link_address = self.get_links_address(dir_path, links)
            linked_bytecode = link_code(unlinked_bytecode, get_link_address)
            try:
                contract = self.web3.eth.contract(abi=abi, bytecode=linked_bytecode)

                # Deploying contract and received transaction hash
                tx_hash = self.deploy_contract(contract)

                address = self.web3.eth.getTransactionReceipt(tx_hash)['contractAddress']
                deployed = {
                    "links": {},
                    "contractAddress": address,
                    "transactionHash": self.web3.toHex(tx_hash)
                }
                link = deployed.get("links")
                for index, get_link in enumerate(list(get_link_address.keys())):
                    link.setdefault(list(get_link_address)[index], get_link_address.get(get_link))
                artifact['networks'].setdefault(self.generate_numbers(), deployed)
                artifact['updatedAt'] = str(datetime.now())

                self.cobra_print("TransactionHash: " + str(self.web3.toHex(tx_hash)), 'success', bold=True)
                self.cobra_print("Address: %s" % str(address), 'success', bold=True)

                artifact = self.web3.toText(dumps(artifact, indent=1).encode())
                return artifact
            except KeyError:
                return None
        else:
            self.cobra_print("[WARNING] Conflict: Already Deployed." + contract[:-5], "warning", bold=True)
            return None

    def deploy_with_out_link(self, dir_path, contract):
        file_path = join(dir_path, contract)
        contract_name = str(contract[:-5])
        artifact_not_loads = self.file_reader(file_path)
        try:
            artifact = loads(artifact_not_loads)
        except json.decoder.JSONDecodeError:
            self.cobra_print("ArtifactDecodeError: %s" % file_path, "error", bold=True)
            sys.exit()

        if not self.isDeployed(artifact):
            self.cobra_print("Deploying " + contract_name + "...", "warning", bold=True)
            abi = artifact['abi']
            bytecode = artifact['bin']
            contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)

            # Deploying contract and received transaction hash
            tx_hash = self.deploy_contract(contract)

            address = self.web3.eth.waitForTransactionReceipt(tx_hash)['contractAddress']
            deployed = {
                "links": dict(),
                "contractAddress": address,
                "transactionHash": self.web3.toHex(tx_hash)
            }
            artifact['networks'].setdefault(self.generate_numbers(), deployed)
            artifact['updatedAt'] = str(datetime.now())

            self.cobra_print("TransactionHash: " + str(self.web3.toHex(tx_hash)), 'success', bold=True)
            self.cobra_print("Address: %s" % str(address), 'success', bold=True)

            artifact = self.web3.toText(dumps(artifact, indent=1).encode())
            return artifact
        else:
            self.cobra_print("[WARNING] Conflict: Already Deployed." + contract[:-5], "warning", bold=True)
            return None
