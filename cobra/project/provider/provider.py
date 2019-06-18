from cobra.project.provider import *


class Provider:

    def __int__(self, network):
        self.network = network
        self.web3 = self.get_web3()
        self.account = self.get_account()
        self.hdwallet = self.get_hdwallet()

    # Get Web3 Instance
    def get_web3(self):
        return Web3(self.get_provider())

    # Provider HTTP, WS or ICP
    def get_provider(self):
        if 'protocol' in self.network:
            if 'HTTP' == self.network['protocol'] or \
                    'http' == self.network['protocol']:
                if not self.get_url_host_port().startswith("http://"):
                    return HTTPProvider(str("http://") + self.get_url_host_port())
                return HTTPProvider(self.get_url_host_port())
            elif 'HTTPS' == self.network['protocol'] or \
                    'https' == self.network['protocol']:
                if not self.get_url_host_port().startswith("https://"):
                    return HTTPProvider(str("https://") + self.get_url_host_port())
                return HTTPProvider(self.get_url_host_port())
            elif 'WS' == self.network['protocol'] or \
                    'ws' == self.network['protocol']:
                if not self.get_url_host_port().startswith("ws://"):
                    return WebsocketProvider(str("ws://") + self.get_url_host_port())
                return WebsocketProvider(self.get_url_host_port())
            elif 'ICP' == self.network['protocol'] or \
                    'icp' == self.network['protocol']:
                return IPCProvider(self.get_url_host_port())
            else:
                if not self.get_url_host_port().startswith("http://"):
                    return HTTPProvider(str("http://") + self.get_url_host_port())
                return HTTPProvider(self.get_url_host_port())
        else:
            console_log("NotFound: Can't find protocol in %s." % 'development',
                        "error")
            sys.exit()

    # Protocol HTTP, WS or ICP
    def get_url_host_port(self):
        if 'host' in self.network and 'port' in self.network:
            return str(self.network['host']) + ':' + str(self.network['port'])
        if 'url' in self.network:
            if 'port' in self.network:
                return str(self.network['url']) + ':' + str(self.network['port'])
            else:
                return str(self.network['url'])

    # Account
    def get_account(self):
        if 'account' in self.network:
            if 'address' in self.network['account']:
                if 'gas' in self.network['account']:
                    if 'gas_price' in self.network['account']:
                        return dict(
                            address=self.network['account']['address'],
                            gas=self.network['account']['gas'],
                            gas_price=self.network['account']['gas_price']
                        )
                    else:
                        return dict(
                            address=self.network['account']['address'],
                            gas=self.network['account']['gas']
                        )
                else:
                    if 'gas_price' in self.network['account']:
                        return dict(
                            address=self.network['account']['address'],
                            gas_price=self.network['account']['gas_price']
                        )
                    else:
                        return dict(
                            address=self.network['account']['address']
                        )
            elif 'gas' in self.network['account']:
                if 'gas_price' in self.network['account']:
                    return dict(
                        gas=self.network['account']['gas'],
                        gas_price=self.network['account']['gas_price']
                    )
                else:
                    return dict(
                        gas=self.network['account']['gas']
                    )
        else:
            return None

    # Get HDWallet
    def get_hdwallet(self):
        if 'hdwallet' in self.network:
            package_checker("cobra-hdwallet",
                            "CobraHDWalletNotFound: install 'pip install cobra-hdwallet'!")
            cobra_hdwallet = __import__("cobra_hdwallet")
            hdwallet = cobra_hdwallet.HDWallet()
            if 'mnemonic' in self.network['hdwallet'] or \
                    'seed' in self.network['hdwallet']:
                if 'password' in self.network['hdwallet']:
                    if 'mnemonic' in self.network['hdwallet']:
                        created_hdwallet = hdwallet.create_hdwallet(
                            mnemonic=self.network['hdwallet']['mnemonic'],
                            passphrase=self.network['hdwallet']['password'])
                        if 'gas' in self.network['hdwallet']:
                            if 'gas_price' in self.network['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.network['hdwallet']['gas'],
                                    gas_price=self.network['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.network['hdwallet']['gas']
                                )
                        else:
                            if 'gas_price' in self.network['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas_price=self.network['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key']
                                )
                    elif 'seed' in self.network['hdwallet']:
                        created_hdwallet = hdwallet.create_hdwallet(
                            mnemonic=self.network['hdwallet']['seed'],
                            passphrase=self.network['hdwallet']['password'])
                        if 'gas' in self.network['hdwallet']:
                            if 'gas_price' in self.network['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.network['hdwallet']['gas'],
                                    gas_price=self.network['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.network['hdwallet']['gas']
                                )
                        else:
                            if 'gas_price' in self.network['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas_price=self.network['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key']
                                )
                else:
                    if 'mnemonic' in self.network['hdwallet']:
                        created_hdwallet = hdwallet.create_hdwallet(
                            mnemonic=self.network['hdwallet']['mnemonic'])
                        if 'gas' in self.network['hdwallet']:
                            if 'gas_price' in self.network['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.network['hdwallet']['gas'],
                                    gas_price=self.network['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.network['hdwallet']['gas']
                                )
                        else:
                            if 'gas_price' in self.network['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas_price=self.network['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key']
                                )
                    elif 'seed' in self.network['hdwallet']:
                        created_hdwallet = hdwallet.create_hdwallet(
                            mnemonic=self.network['hdwallet']['seed'])
                        if 'gas' in self.network['hdwallet']:
                            if 'gas_price' in self.network['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.network['hdwallet']['gas'],
                                    gas_price=self.network['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.network['hdwallet']['gas']
                                )
                        else:
                            if 'gas_price' in self.network['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas_price=self.network['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key']
                                )
            elif 'private' in self.network['hdwallet']:
                try:
                    created_hdwallet = hdwallet.hdwallet_from_private(
                        private=self.network['hdwallet']['private'])
                    if 'gas' in self.network['hdwallet']:
                        if 'gas_price' in self.network['hdwallet']:
                            return dict(
                                address=created_hdwallet['address'],
                                public_key=created_hdwallet['public_key'],
                                private_key=created_hdwallet['private_key'],
                                gas=self.network['hdwallet']['gas'],
                                gas_price=self.network['hdwallet']['gas_price']
                            )
                        else:
                            return dict(
                                address=created_hdwallet['address'],
                                public_key=created_hdwallet['public_key'],
                                private_key=created_hdwallet['private_key'],
                                gas=self.network['hdwallet']['gas']
                            )
                    else:
                        if 'gas_price' in self.network['hdwallet']:
                            return dict(
                                address=created_hdwallet['address'],
                                public_key=created_hdwallet['public_key'],
                                private_key=created_hdwallet['private_key'],
                                gas_price=self.network['hdwallet']['gas_price']
                            )
                        else:
                            return dict(
                                address=created_hdwallet['address'],
                                public_key=created_hdwallet['public_key'],
                                private_key=created_hdwallet['private_key'],
                            )
                except ValueError:
                    console_log("ValueError: Bad private key, if length must be 64!",
                                "error")
                    sys.exit()
        else:
            return None
