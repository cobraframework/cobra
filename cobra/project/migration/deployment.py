from cobra.project.migration import *
import web3


class Deployment(Provider):

    def __init__(self, _network, more=False):
        self.more = more
        self.network = _network
        self.web3 = self.get_web3()
        self.account = self.get_account()
        self.hdwallet = self.get_hdwallet()

    def get_transact(self, artifact):
        try:
            networks = artifact["networks"]
            if networks:
                for __network in networks.keys():
                    deployed = networks.get(__network)
                    if "contractAddress" in deployed and "transactionHash" in deployed:
                        if deployed["contractAddress"] == "Unknown" and deployed["transactionHash"]:
                            try:
                                get_transaction_receipt = self.web3.eth\
                                    .getTransactionReceipt(deployed["transactionHash"])
                                if get_transaction_receipt:
                                    deployed["contractAddress"] = get_transaction_receipt["contractAddress"]
                                    artifact['updatedAt'] = str(datetime.now())
                                else:
                                    continue
                            except ValueError:
                                continue
                        else:
                            continue
                    else:
                        continue
            return artifact
        except requests.exceptions.ConnectionError:
            console_log(
                "'%s' failed!" % (self.get_url_host_port()),
                "error", "HTTPConnectionPool")
            sys.exit()
        except websockets.exceptions.InvalidMessage:
            console_log(
                "'%s' failed!" % (self.get_url_host_port()),
                "error", "WebSocketsConnectionPool")
            sys.exit()
        except FileNotFoundError:
            console_log(
                "'%s' failed!" % (self.get_url_host_port()),
                "error", "ICPConnectionPool")
            sys.exit()
        except KeyError as key_error:
            console_log(str(key_error), "error", "KeyError")
            sys.exit()

    def is_deployed(self, artifact):
        try:
            networks = artifact['networks']
            if networks:
                for __network in networks.keys():
                    deployed = networks.get(__network)
                    try:
                        deployed_web3 = self.web3.eth.getTransactionReceipt(deployed['transactionHash'])
                        if deployed['contractAddress'] == deployed_web3['contractAddress']:
                            return True
                        else:
                            continue
                    except TypeError:
                        continue
            else:
                self.web3.eth.getTransactionReceipt(str())
                return False
        except requests.exceptions.ConnectionError:
            console_log(
                "'%s' failed!" % (self.get_url_host_port()),
                "error", "HTTPConnectionPool")
            sys.exit()
        except websockets.exceptions.InvalidMessage:
            console_log(
                "'%s' failed!" % (self.get_url_host_port()),
                "error", "WebSocketsConnectionPool")
            sys.exit()
        except FileNotFoundError:
            console_log(
                "'%s' failed!" % (self.get_url_host_port()),
                "error", "ICPConnectionPool")
            sys.exit()
        except KeyError:
            return False

    def get_links_address(self, dir_path, links):
        contract_name_and_address = dict()
        contract_name_and_unknown_address = dict()
        for link in links:
            link_file_path = join(dir_path, link)
            artifact_not_loads = file_reader(link_file_path)
            try:
                artifact = loads(artifact_not_loads)
                if 'networks' in artifact:
                    networks = artifact['networks']
                    if not networks:
                        link_name = link[:-5]
                        contract_name_and_unknown_address.setdefault(link_name, "Unknown")
                        continue
                    for __network in networks.keys():
                        deployed = networks.get(__network)
                        if "contractAddress" in deployed and "transactionHash" in deployed:
                            try:
                                if deployed["contractAddress"] and deployed["transactionHash"]:
                                    deployed_web3 = self.web3.eth.getTransactionReceipt(deployed['transactionHash'])
                                    if deployed_web3 is not None:  # TypeError
                                        if deployed['contractAddress'] == deployed_web3['contractAddress']:
                                            link_name = link[:-5]
                                            contract_name_and_address.setdefault(link_name, deployed['contractAddress'])
                                        else:
                                            link_name = link[:-5]
                                            contract_name_and_unknown_address.setdefault(link_name, "Unknown")
                                    elif deployed['contractAddress'] == "Unknown":
                                        link_name = link[:-5]
                                        contract_name_and_unknown_address.setdefault(link_name, "Unknown")
                            except ValueError:
                                continue
                        else:
                            continue
                else:
                    console_log("networks in %s" % str(link), "error", "NotFound")
            except json.decoder.JSONDecodeError as jsonDecodeError:
                console_log(str(jsonDecodeError), "error", "JSONDecodeError")
                sys.exit()
        return contract_name_and_address, contract_name_and_unknown_address

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
                tx_hash = contract.constructor().transact(transaction=transaction)
                return tx_hash
        except ValueError as valueError:
            value_error = valueError.args.__getitem__(0)
            if 'message' in value_error and not self.more:
                message = str(value_error['message'])
                split_message = message.split('\n')
                console_log("%s" % split_message[0],
                            "error")
            elif 'message' in value_error and self.more:
                message = str(value_error['message'])
                console_log("%s" % message,
                            "error")
            elif not self.more:
                message = str(value_error)
                console_log("%s..." % message[:75],
                            "error")
            elif self.more:
                message = str(value_error)
                console_log("%s..." % message,
                            "error")
            sys.exit()

    @staticmethod
    def check_unknown_addresses(link_unknown_address):
        if isinstance(link_unknown_address, dict) and link_unknown_address:
            for contract_name in link_unknown_address.keys():
                console_log(title="Unknown", _type="error",
                            text="%s link address!" % str(contract_name))
            sys.exit()
        return

    def deploy_with_link(self, dir_path, contract, links, more=False):

        contract_name = str(contract[:-5])
        file_path = join(dir_path, contract)
        artifact_not_loads = file_reader(file_path)

        try:
            _artifact = loads(artifact_not_loads)
        except json.decoder.JSONDecodeError as jsonDecodeError:
            console_log("%s" % jsonDecodeError, "error", "JSONDecodeError")
            return

        artifact = self.get_transact(_artifact)
        if not self.is_deployed(artifact):
            console_log("Deploying " + contract_name + "...")
            abi = artifact['abi']
            unlinked_bytecode = artifact['bin']
            get_link_address, get_link_unknown_address = self.get_links_address(dir_path, links)
            self.check_unknown_addresses(get_link_unknown_address)
            linked_bytecode = link_code(unlinked_bytecode, get_link_address)
            try:
                contract = self.web3.eth.contract(abi=abi, bytecode=linked_bytecode)

                # Deploying contract and received transaction hash
                try:
                    tx_hash = self.deploy_contract(contract)
                except requests.exceptions.ConnectionError:
                    console_log(
                        "'%s' failed!" % (self.get_url_host_port()),
                        "error", "HTTPConnectionPool")
                    sys.exit()
                except websockets.exceptions.InvalidMessage:
                    console_log(
                        "'%s' failed!" % (self.get_url_host_port()),
                        "error", "WebSocketsConnectionPool")
                    sys.exit()
                except FileNotFoundError:
                    console_log(
                        "'%s' failed!" % (self.get_url_host_port()),
                        "error", "ICPConnectionPool")
                    sys.exit()
                try:
                    transaction_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash, timeout=360)
                    address = transaction_receipt['contractAddress']
                    deployed = {
                        "links": dict(),
                        "contractAddress": address,
                        "transactionHash": self.web3.toHex(tx_hash)
                    }
                    link = deployed.get("links")
                    for index, get_link in enumerate(list(get_link_address.keys())):
                        link.setdefault(list(get_link_address)[index], get_link_address.get(get_link))
                    artifact['networks'].setdefault(generate_numbers(), deployed)
                    artifact['updatedAt'] = str(datetime.now())

                    console_log(title="Deploy",
                                text="%s done!" % contract_name, _type="success")
                    console_log(title="TransactionHash", space=True,
                                text=str(self.web3.toHex(tx_hash)), _type="success")
                    console_log(title="Address", space=True,
                                text=str(address), _type="success")

                    artifact = self.web3.toText(dumps(artifact, indent=1).encode())
                    return artifact
                except web3.utils.threads.Timeout as timeout:
                    address = "Unknown"
                    deployed = {
                        "links": dict(),
                        "contractAddress": address,
                        "transactionHash": self.web3.toHex(tx_hash)
                    }
                    link = deployed.get("links")
                    for index, get_link in enumerate(list(get_link_address.keys())):
                        link.setdefault(list(get_link_address)[index], get_link_address.get(get_link))
                    artifact['networks'].setdefault(generate_numbers(), deployed)
                    artifact['updatedAt'] = str(datetime.now())

                    console_log(title="Deploy",
                                text="%s not done!" % contract_name, _type="warning")
                    console_log(title="TransactionHash", space=True,
                                text=str(self.web3.toHex(tx_hash)), _type="warning")
                    console_log(title="Address", space=True,
                                text=str(address), _type="warning")
                    console_log(title="Timeout", _type="error",
                                text="%s, %s still on mining!" % (str(timeout),
                                                                  str(self.web3.toHex(tx_hash))))

                    artifact = self.web3.toText(dumps(artifact, indent=1).encode())
                    return artifact
            except KeyError:
                artifact = self.web3.toText(dumps(artifact, indent=1).encode())
                return artifact
        else:
            console_log(title="Deploy", text="Already deployed.%s" %
                                             contract_name, _type="warning")
            artifact = self.web3.toText(dumps(artifact, indent=1).encode())
            return artifact

    def deploy_with_out_link(self, dir_path, contract, more=False):

        file_path = join(dir_path, contract)
        contract_name = str(contract[:-5])
        artifact_not_loads = file_reader(file_path)
        try:
            _artifact = loads(artifact_not_loads)
        except json.decoder.JSONDecodeError as jsonDecodeError:
            console_log(jsonDecodeError, "error", "JSONDecodeError")
            sys.exit()

        artifact = self.get_transact(_artifact)
        if not self.is_deployed(artifact):
            console_log("Deploying " + contract_name + "...")
            abi = artifact['abi']
            bytecode = artifact['bin']
            contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)

            # Deploying contract and received transaction hash
            try:
                tx_hash = self.deploy_contract(contract)
            except requests.exceptions.ConnectionError:
                console_log(
                    "'%s' failed!" % (self.get_url_host_port()),
                    "error", "HTTPConnectionPool")
                sys.exit()
            except websockets.exceptions.InvalidMessage:
                console_log(
                    "'%s' failed!" % (self.get_url_host_port()),
                    "error", "WebSocketsConnectionPool")
                sys.exit()
            except FileNotFoundError:
                console_log(
                    "'%s' failed!" % (self.get_url_host_port()),
                    "error", "ICPConnectionPool")
                sys.exit()

            try:
                transaction_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash, timeout=360)
                address = transaction_receipt['contractAddress']
                deployed = {
                    "links": dict(),
                    "contractAddress": address,
                    "transactionHash": self.web3.toHex(tx_hash)
                }
                artifact['networks'].setdefault(generate_numbers(), deployed)
                artifact['updatedAt'] = str(datetime.now())

                console_log(title="Deploy",
                            text="%s done!" % contract_name, _type="success")
                console_log(title="TransactionHash", space=True,
                            text=str(self.web3.toHex(tx_hash)), _type="success")
                console_log(title="Address", space=True,
                            text=str(address), _type="success")

                artifact = self.web3.toText(dumps(artifact, indent=1).encode())
                return artifact
            except web3.utils.threads.Timeout as timeout:
                address = "Unknown"
                deployed = {
                    "links": dict(),
                    "contractAddress": address,
                    "transactionHash": self.web3.toHex(tx_hash)
                }
                artifact['networks'].setdefault(generate_numbers(), deployed)
                artifact['updatedAt'] = str(datetime.now())

                console_log(title="Deploy",
                            text="%s not done!" % contract_name, _type="warning")
                console_log(title="TransactionHash", space=True,
                            text=str(self.web3.toHex(tx_hash)), _type="warning")
                console_log(title="Address", space=True,
                            text=str(address), _type="warning")
                console_log(title="Timeout", _type="error",
                            text="%s, %s still on mining!" % (str(timeout),
                                                              str(self.web3.toHex(tx_hash))))

                artifact = self.web3.toText(dumps(artifact, indent=1).encode())
                return artifact
        else:
            console_log(title="Deploy", text="Already deployed.%s" %
                                             contract_name, _type="warning")
            artifact = self.web3.toText(dumps(artifact, indent=1).encode())
            return artifact
