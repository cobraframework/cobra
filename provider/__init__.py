from lazyme.string import color_print
from web3 import Web3, HTTPProvider, \
    WebsocketProvider, IPCProvider
from colorama import Fore, Style
import pkg_resources
import sys


class CobraProvider:

    def __int__(self, cobraNetwork):
        self.cobraNetwork = cobraNetwork
        self.web3 = self.get_web3()
        self.account = self.get_account()
        self.hdwallet = self.get_hdwallet()

    def cobra_print(self, text, color=None):
        # Checking text instance is string
        if isinstance(text, str):
            if color == 'success':
                return print(Style.DIM + Fore.GREEN + '[SUCCESS]' + Style.RESET_ALL + ' ' + text)
            elif color == 'warning':
                return print(Style.DIM + Fore.YELLOW + '[WARNING]' + Style.RESET_ALL + ' ' + text)
            elif color == 'error':
                return print(Style.DIM + Fore.RED + '[ERROR]' + Style.RESET_ALL + ' ' + text)
            else:
                return print(text)

    # Get Web3 Instance
    def get_web3(self):
        return Web3(self.get_provider())

    # Package Checker
    def package_checker(self, package_name: str, error_message: str):
        package = False
        installed_packages = pkg_resources.working_set
        package_keys = sorted(['%s' % installed_package.key
                               for installed_package in installed_packages])
        for package_key in package_keys:
            if package_key == package_name:
                package = True

        if not package:
            if error_message:
                self.cobra_print(error_message, "error")
            sys.exit()

    # Provider HTTP, WS or ICP
    def get_provider(self):
        if 'protocol' in self.cobraNetwork:
            if 'HTTP' == self.cobraNetwork['protocol'] or \
                    'http' == self.cobraNetwork['protocol']:
                if not self.get_url_host_port().startswith("http://"):
                    return HTTPProvider(str("http://") + self.get_url_host_port())
                return HTTPProvider(self.get_url_host_port())
            elif 'HTTPS' == self.cobraNetwork['protocol'] or \
                    'https' == self.cobraNetwork['protocol']:
                if not self.get_url_host_port().startswith("https://"):
                    return HTTPProvider(str("https://") + self.get_url_host_port())
                return HTTPProvider(self.get_url_host_port())
            elif 'WS' == self.cobraNetwork['protocol'] or \
                    'ws' == self.cobraNetwork['protocol']:
                if not self.get_url_host_port().startswith("ws://"):
                    return WebsocketProvider(str("ws://") + self.get_url_host_port())
                return WebsocketProvider(self.get_url_host_port())
            elif 'ICP' == self.cobraNetwork['protocol'] or \
                    'icp' == self.cobraNetwork['protocol']:
                return IPCProvider(self.get_url_host_port())
            else:
                if not self.get_url_host_port().startswith("http://"):
                    return HTTPProvider(str("http://") + self.get_url_host_port())
                return HTTPProvider(self.get_url_host_port())
        else:
            self.cobra_print("NotFound: Can't find protocol in %s." % 'development',
                             "error")
            sys.exit()

    # Protocol HTTP, WS or ICP
    def get_url_host_port(self):
        if 'host' in self.cobraNetwork and 'port' in self.cobraNetwork:
            return str(self.cobraNetwork['host']) + ':' + str(self.cobraNetwork['port'])
        if 'url' in self.cobraNetwork:
            if 'port' in self.cobraNetwork:
                return str(self.cobraNetwork['url']) + ':' + str(self.cobraNetwork['port'])
            else:
                return str(self.cobraNetwork['url'])
            
    # Account
    def get_account(self):
        if 'account' in self.cobraNetwork:
            if 'address' in self.cobraNetwork['account']:
                if 'gas' in self.cobraNetwork['account']:
                    if 'gas_price' in self.cobraNetwork['account']:
                        return dict(
                            address=self.cobraNetwork['account']['address'],
                            gas=self.cobraNetwork['account']['gas'],
                            gas_price=self.cobraNetwork['account']['gas_price']
                        )
                    else:
                        return dict(
                            address=self.cobraNetwork['account']['address'],
                            gas=self.cobraNetwork['account']['gas']
                        )
                else:
                    if 'gas_price' in self.cobraNetwork['account']:
                        return dict(
                            address=self.cobraNetwork['account']['address'],
                            gas_price=self.cobraNetwork['account']['gas_price']
                        )
                    else:
                        return dict(
                            address=self.cobraNetwork['account']['address']
                        )
            elif 'gas' in self.cobraNetwork['account']:
                if 'gas_price' in self.cobraNetwork['account']:
                    return dict(
                        gas=self.cobraNetwork['account']['gas'],
                        gas_price=self.cobraNetwork['account']['gas_price']
                    )
                else:
                    return dict(
                        gas=self.cobraNetwork['account']['gas']
                    )
        else:
            return None

    # Get HDWallet
    def get_hdwallet(self):
        if 'hdwallet' in self.cobraNetwork:
            self.package_checker("cobra-hdwallet",
                                 "CobraHDWalletNotFound: install 'pip install cobra-hdwallet'!")
            cobra_hdwallet = __import__("cobra_hdwallet")
            hdWallet = cobra_hdwallet.HDWallet()
            if 'mnemonic' in self.cobraNetwork['hdwallet'] or \
                    'seed' in self.cobraNetwork['hdwallet']:
                if 'password' in self.cobraNetwork['hdwallet']:
                    if 'mnemonic' in self.cobraNetwork['hdwallet']:
                        created_hdwallet = hdWallet.create_hdwallet(
                            mnemonic=self.cobraNetwork['hdwallet']['mnemonic'],
                            passphrase=self.cobraNetwork['hdwallet']['password'])
                        if 'gas' in self.cobraNetwork['hdwallet']:
                            if 'gas_price' in self.cobraNetwork['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.cobraNetwork['hdwallet']['gas'],
                                    gas_price=self.cobraNetwork['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.cobraNetwork['hdwallet']['gas']
                                )
                        else:
                            if 'gas_price' in self.cobraNetwork['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas_price=self.cobraNetwork['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key']
                                )
                    elif 'seed' in self.cobraNetwork['hdwallet']:
                        created_hdwallet = hdWallet.create_hdwallet(
                            mnemonic=self.cobraNetwork['hdwallet']['seed'],
                            passphrase=self.cobraNetwork['hdwallet']['password'])
                        if 'gas' in self.cobraNetwork['hdwallet']:
                            if 'gas_price' in self.cobraNetwork['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.cobraNetwork['hdwallet']['gas'],
                                    gas_price=self.cobraNetwork['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.cobraNetwork['hdwallet']['gas']
                                )
                        else:
                            if 'gas_price' in self.cobraNetwork['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas_price=self.cobraNetwork['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key']
                                )
                else:
                    if 'mnemonic' in self.cobraNetwork['hdwallet']:
                        created_hdwallet = hdWallet.create_hdwallet(
                            mnemonic=self.cobraNetwork['hdwallet']['mnemonic'])
                        if 'gas' in self.cobraNetwork['hdwallet']:
                            if 'gas_price' in self.cobraNetwork['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.cobraNetwork['hdwallet']['gas'],
                                    gas_price=self.cobraNetwork['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.cobraNetwork['hdwallet']['gas']
                                )
                        else:
                            if 'gas_price' in self.cobraNetwork['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas_price=self.cobraNetwork['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key']
                                )
                    elif 'seed' in self.cobraNetwork['hdwallet']:
                        created_hdwallet = hdWallet.create_hdwallet(
                            mnemonic=self.cobraNetwork['hdwallet']['seed'])
                        if 'gas' in self.cobraNetwork['hdwallet']:
                            if 'gas_price' in self.cobraNetwork['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.cobraNetwork['hdwallet']['gas'],
                                    gas_price=self.cobraNetwork['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas=self.cobraNetwork['hdwallet']['gas']
                                )
                        else:
                            if 'gas_price' in self.cobraNetwork['hdwallet']:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key'],
                                    gas_price=self.cobraNetwork['hdwallet']['gas_price']
                                )
                            else:
                                return dict(
                                    address=created_hdwallet['address'],
                                    public_key=created_hdwallet['public_key'],
                                    private_key=created_hdwallet['private_key']
                                )
            elif 'private' in self.cobraNetwork['hdwallet']:
                try:
                    created_hdwallet = hdWallet.hdwallet_from_private(
                        private=self.cobraNetwork['hdwallet']['private'])
                    if 'gas' in self.cobraNetwork['hdwallet']:
                        if 'gas_price' in self.cobraNetwork['hdwallet']:
                            return dict(
                                address=created_hdwallet['address'],
                                public_key=created_hdwallet['public_key'],
                                private_key=created_hdwallet['private_key'],
                                gas=self.cobraNetwork['hdwallet']['gas'],
                                gas_price=self.cobraNetwork['hdwallet']['gas_price']
                            )
                        else:
                            return dict(
                                address=created_hdwallet['address'],
                                public_key=created_hdwallet['public_key'],
                                private_key=created_hdwallet['private_key'],
                                gas=self.cobraNetwork['hdwallet']['gas']
                            )
                    else:
                        if 'gas_price' in self.cobraNetwork['hdwallet']:
                            return dict(
                                address=created_hdwallet['address'],
                                public_key=created_hdwallet['public_key'],
                                private_key=created_hdwallet['private_key'],
                                gas_price=self.cobraNetwork['hdwallet']['gas_price']
                            )
                        else:
                            return dict(
                                address=created_hdwallet['address'],
                                public_key=created_hdwallet['public_key'],
                                private_key=created_hdwallet['private_key'],
                            )
                except ValueError:
                    self.cobra_print("ValueError: Bad private key, if length must be 64!",
                                     "error")
                    sys.exit()
        else:
            return None
