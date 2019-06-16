from colorama import Fore, Style
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

ACCOUNT_TEXT = """Balance: %d
Address: %s"""
HDWALLET_TEXT = """Balance: %d
Address: %s
Public Key: %s
Private Key: %s"""


class CobraDeploy(CobraProvider):
    network = """{,
     "network": {},
     "updatedAt": "%s"
    }""" % str(datetime.now())

    def __init__(self, cobraNetwork, more=False):
        self.more = more
        self.cobraNetwork = cobraNetwork
        self.web3 = self.get_web3()
        self.account = self.get_account()
        self.hdwallet = self.get_hdwallet()
        # self.display_account()

    def display_account(self):
        if self.account is not None:
            self.cobra_print(ACCOUNT_TEXT % (self.web3.eth.getBalance(self.account['address']),
                                             self.web3.toChecksumAddress(self.account['address'])))
        elif self.hdwallet is not None:
            self.cobra_print(HDWALLET_TEXT % (self.web3.eth.getBalance(self.hdwallet['address']),
                                              self.web3.toChecksumAddress(self.hdwallet['address']),
                                              self.hdwallet['public_key'],
                                              self.hdwallet['private_key']))
        else:
            self.cobra_print(ACCOUNT_TEXT % self.web3.eth.accounts[0])

    def file_reader(self, file_path):
        try:
            with open(file_path, 'r') as read_file:
                return_file = read_file.read()
                read_file.close()
                return return_file
        except FileNotFoundError:
            self.cobra_print(file_path, "error", "FileNotFound")
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
                        "'%s' failed!" % (self.get_url_host_port()),
                        "error", "HTTPConnectionPool")
                    sys.exit()
                except websockets.exceptions.InvalidMessage:
                    self.cobra_print(
                        "'%s' failed!" % (self.get_url_host_port()),
                        "error", "WebSocketsConnectionPool")
                    sys.exit()
                except FileNotFoundError:
                    self.cobra_print(
                        "'%s' failed!" % (self.get_url_host_port()),
                        "error", "ICPConnectionPool")
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
            except json.decoder.JSONDecodeError as jsonDecodeError:
                self.cobra_print(str(jsonDecodeError), "error", "JSONDecodeError")
                return
        return contract_name_and_address

    def deploy_contract(self, contract):
        try:
            if self.account is not None:
                # self.web3.personal.unlockAccount(self.hdwallet['private_key'], None)
                if 'gas' in self.account:
                    if 'gas_price' in self.account:
                        transaction = {
                            'from': self.web3.toChecksumAddress(self.account['address']),
                            'gas': self.account['gas'],
                            'gasPrice': self.account['gas_price']
                        }
                        tx_hash = contract.deploy(transaction=transaction)
                        return tx_hash
                    else:
                        transaction = {
                            'from': self.web3.toChecksumAddress(self.account['address']),
                            'gas': self.account['gas'],
                            'gasPrice': self.web3.eth.gasPrice
                        }
                        tx_hash = contract.deploy(transaction=transaction)
                        return tx_hash
                else:
                    if 'gas_price' in self.account:
                        transaction = {
                            'from': self.web3.toChecksumAddress(self.account['address']),
                            'gas': 3000000,
                            'gasPrice': self.account['gas_price']
                        }
                        tx_hash = contract.deploy(transaction=transaction)
                        return tx_hash
                    else:
                        transaction = {
                            'from': self.web3.toChecksumAddress(self.account['address']),
                            'gas': 3000000,
                            'gasPrice': self.web3.eth.gasPrice
                        }
                        tx_hash = contract.deploy(transaction=transaction)
                        return tx_hash
            elif self.hdwallet is not None:
                if 'gas' in self.hdwallet:
                    if 'gas_price' in self.hdwallet:
                        account = self.web3.eth.account.privateKeyToAccount(self.hdwallet['private_key'])
                        construct_txn = contract.constructor().buildTransaction({
                            'from': account.address,
                            'value': 0,
                            'nonce': self.web3.eth.getTransactionCount(account.address),
                            'gas': self.hdwallet['gas'],
                            'gasPrice': self.hdwallet['gas_price']
                        })
                        signed = account.signTransaction(construct_txn)
                        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
                        return tx_hash
                    else:
                        account = self.web3.eth.account.privateKeyToAccount(self.hdwallet['private_key'])
                        construct_txn = contract.constructor().buildTransaction({
                            'from': account.address,
                            'value': 0,
                            'nonce': self.web3.eth.getTransactionCount(account.address),
                            'gas': self.hdwallet['gas'],
                            'gasPrice': self.web3.eth.gasPrice
                        })
                        signed = account.signTransaction(construct_txn)
                        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
                        return tx_hash
                else:
                    if 'gas_price' in self.hdwallet:
                        account = self.web3.eth.account.privateKeyToAccount(self.hdwallet['private_key'])
                        construct_txn = contract.constructor().buildTransaction({
                            'from': account.address,
                            'value': 0,
                            'nonce': self.web3.eth.getTransactionCount(account.address),
                            'gas': 3000000,
                            'gasPrice': self.hdwallet['gas_price']
                        })
                        signed = account.signTransaction(construct_txn)
                        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
                        return tx_hash
                    else:
                        account = self.web3.eth.account.privateKeyToAccount(self.hdwallet['private_key'])
                        construct_txn = contract.constructor().buildTransaction({
                            'from': account.address,
                            'value': 0,
                            'nonce': self.web3.eth.getTransactionCount(account.address),
                            'gas': 3000000,
                            'gasPrice': self.web3.eth.gasPrice
                        })
                        signed = account.signTransaction(construct_txn)
                        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
                        return tx_hash
            else:
                transaction = {
                    'from': self.web3.eth.accounts[0],
                    'gas': 3000000,
                    'gasPrice': self.web3.eth.gasPrice
                }
                tx_hash = contract.deploy(transaction=transaction)
                return tx_hash
        except ValueError as valueError:
            valueError = valueError.args.__getitem__(0)
            if 'message' in valueError and not self.more:
                message = str(valueError['message'])
                split_message = message.split('\n')
                self.cobra_print("%s" % split_message[0],
                                 "error")
            elif 'message' in valueError and self.more:
                message = str(valueError['message'])
                self.cobra_print("%s" % message,
                                 "error")
            elif not self.more:
                message = str(valueError)
                self.cobra_print("%s..." % message[:75],
                                 "error")
            elif self.more:
                message = str(valueError)
                self.cobra_print("%s..." % message,
                                 "error")
            sys.exit()

    def deploy_with_link(self, dir_path, contract, links, more=False):

        contract_name = str(contract[:-5])
        file_path = join(dir_path, contract)
        artifact_not_loads = self.file_reader(file_path)

        try:
            artifact = loads(artifact_not_loads)
        except json.decoder.JSONDecodeError as jsonDecodeError:
            self.cobra_print("%s" % jsonDecodeError, "error", "JSONDecodeError")
            return

        if not self.isDeployed(artifact):
            self.cobra_print("Deploying " + contract_name + "...")
            abi = artifact['abi']
            unlinked_bytecode = artifact['bin']
            get_link_address = self.get_links_address(dir_path, links)
            linked_bytecode = link_code(unlinked_bytecode, get_link_address)
            try:
                contract = self.web3.eth.contract(abi=abi, bytecode=linked_bytecode)

                # Deploying contract and received transaction hash
                try:
                    tx_hash = self.deploy_contract(contract)
                except requests.exceptions.ConnectionError:
                    self.cobra_print(
                        "'%s' failed!" % (self.get_url_host_port()),
                        "error", "HTTPConnectionPool")
                    sys.exit()
                except websockets.exceptions.InvalidMessage:
                    self.cobra_print(
                        "'%s' failed!" % (self.get_url_host_port()),
                        "error", "WebSocketsConnectionPool")
                    sys.exit()
                except FileNotFoundError:
                    self.cobra_print(
                        "'%s' failed!" % (self.get_url_host_port()),
                        "error", "ICPConnectionPool")
                    sys.exit()

                transactionReceipt = self.web3.eth.waitForTransactionReceipt(tx_hash, timeout=120)
                address = transactionReceipt['contractAddress']
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

                self.cobra_print(title="Deploy",
                                 text="%s done!" % contract_name, type="success")
                self.cobra_print(title="TransactionHash", space=True,
                                 text=str(self.web3.toHex(tx_hash)), type="success")
                self.cobra_print(title="Address", space=True,
                                 text=str(address), type="success")

                artifact = self.web3.toText(dumps(artifact, indent=1).encode())
                return artifact
            except KeyError:
                return None
        else:
            self.cobra_print(title="Deploy", text="Already deployed.%s" %
                                                  contract_name, type="warning")
            return None

    def deploy_with_out_link(self, dir_path, contract, more=False):

        file_path = join(dir_path, contract)
        contract_name = str(contract[:-5])
        artifact_not_loads = self.file_reader(file_path)
        try:
            artifact = loads(artifact_not_loads)
        except json.decoder.JSONDecodeError as jsonDecodeError:
            self.cobra_print(jsonDecodeError, "error", "JSONDecodeError")
            sys.exit()

        if not self.isDeployed(artifact):
            self.cobra_print("Deploying " + contract_name + "...")
            abi = artifact['abi']
            bytecode = artifact['bin']
            contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)

            # Deploying contract and received transaction hash
            try:
                tx_hash = self.deploy_contract(contract)
            except requests.exceptions.ConnectionError:
                self.cobra_print(
                    "'%s' failed!" % (self.get_url_host_port()),
                    "error", "HTTPConnectionPool")
                sys.exit()
            except websockets.exceptions.InvalidMessage:
                self.cobra_print(
                    "'%s' failed!" % (self.get_url_host_port()),
                    "error", "WebSocketsConnectionPool")
                sys.exit()
            except FileNotFoundError:
                self.cobra_print(
                    "'%s' failed!" % (self.get_url_host_port()),
                    "error", "ICPConnectionPool")
                sys.exit()

            transactionReceipt = self.web3.eth.waitForTransactionReceipt(tx_hash, timeout=120)
            address = transactionReceipt['contractAddress']
            deployed = {
                "links": dict(),
                "contractAddress": address,
                "transactionHash": self.web3.toHex(tx_hash)
            }
            artifact['networks'].setdefault(self.generate_numbers(), deployed)
            artifact['updatedAt'] = str(datetime.now())

            self.cobra_print(title="Deploy",
                             text="%s done!" % contract_name, type="success")
            self.cobra_print(title="TransactionHash", space=True,
                             text=str(self.web3.toHex(tx_hash)), type="success")
            self.cobra_print(title="Address", space=True,
                             text=str(address), type="success")

            artifact = self.web3.toText(dumps(artifact, indent=1).encode())
            return artifact
        else:
            self.cobra_print(title="Deploy", text="Already deployed.%s" %
                                                  contract_name, type="warning")
            return None
