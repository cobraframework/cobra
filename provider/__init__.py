from lazyme.string import color_print
from web3 import Web3, HTTPProvider, \
    WebsocketProvider, IPCProvider
import pkg_resources
import sys


class CobraProvider:

    # def __init__(self):
    #     pass

    def __int__(self, cobraNetwork):
        self.cobraNetwork = cobraNetwork
        self.web3 = self.get_web3()
        self.account = self.get_account()
        self.hdwallet = self.get_hdwallet()

    def cobra_print(self, text, color=None, bold=False, background=None, underline=False):
        if color == 'success':
            return color_print(text, color='green', bold=bold, highlighter=background, underline=underline)
        elif color == 'warning':
            return color_print(text, color='yellow', bold=bold, highlighter=background, underline=underline)
        elif color == 'error':
            return color_print(text, color='red', bold=bold, highlighter=background, underline=underline)
        else:
            return color_print(text, bold=bold, highlighter=background, underline=underline)

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
                self.cobra_print(error_message, "error", bold=True)
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
                    return dict(
                        address=self.cobraNetwork['account']['address'],
                        gas=self.cobraNetwork['account']['gas']
                    )
                else:
                    return dict(
                        address=self.cobraNetwork['account']['address']
                    )
            elif 'gas' in self.cobraNetwork['account']:
                return dict(
                    gas=self.cobraNetwork['account']['gas']
                )
        else:
            return None

    # HDWallet
    def get_hdwallet(self):
        if 'hdwallet' in self.cobraNetwork:
            self.package_checker("cobra-hdwallet",
                                 "[ERROR] CobraHDWalletNotFound: install 'pip install cobra-hdwallet'!")
            cobra_hdwallet = __import__("cobra_hdwallet")
            hdWallet = cobra_hdwallet.HDWallet()
            if 'mnemonic' in self.cobraNetwork['hdwallet'] or \
                    'seed' in self.cobraNetwork['hdwallet']:
                if 'password' in self.cobraNetwork['hdwallet']:
                    if 'mnemonic' in self.cobraNetwork['hdwallet']:
                        created_hdwallet = hdWallet.create_hdwallet(
                            mnemonic=self.cobraNetwork['hdwallet']['mnemonic'],
                            password=self.cobraNetwork['hdwallet']['password'])
                        return created_hdwallet
                    elif 'seed' in self.cobraNetwork['hdwallet']:
                        created_hdwallet = hdWallet.create_hdwallet(
                            mnemonic=self.cobraNetwork['hdwallet']['seed'],
                            password=self.cobraNetwork['hdwallet']['password'])
                        return created_hdwallet
                else:
                    if 'mnemonic' in self.cobraNetwork['hdwallet']:
                        created_hdwallet = hdWallet.create_hdwallet(
                            mnemonic=self.cobraNetwork['hdwallet']['mnemonic'])
                        return created_hdwallet
                    elif 'seed' in self.cobraNetwork['hdwallet']:
                        created_hdwallet = hdWallet.create_hdwallet(
                            mnemonic=self.cobraNetwork['hdwallet']['seed'])
                        return created_hdwallet
            elif 'private' in self.cobraNetwork['hdwallet']:
                created_hdwallet = hdWallet.hdwallet_from_private(
                    mnemonic=self.cobraNetwork['hdwallet']['private'])
                return created_hdwallet
        else:
            return None
