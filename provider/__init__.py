from lazyme.string import color_print
from web3 import Web3, HTTPProvider
import pkg_resources
import sys


class CobraProvider:

    def __int__(self, cobraNetwork):
        self.cobraNetwork = cobraNetwork
        self.main()

    def cobra_print(self, text, color=None, bold=False, background=None, underline=False):
        if color == 'success':
            return color_print(text, color='green', bold=bold, highlighter=background, underline=underline)
        elif color == 'warning':
            return color_print(text, color='yellow', bold=bold, highlighter=background, underline=underline)
        elif color == 'error':
            return color_print(text, color='red', bold=bold, highlighter=background, underline=underline)
        else:
            return color_print(text, bold=bold, highlighter=background, underline=underline)

    def main(self):
        pass

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
                self.cobra_print(error_message,
                                 "error", bold=True)
            sys.exit()

    # Protocol HTTP, WS or ICP
    def get_protocol(self):
        if 'protocol' in self.cobraNetwork:
            if 'HTTP' == self.cobraNetwork['protocol'] or \
                    'http' == self.cobraNetwork['protocol']:
                return 'HTTP'
            elif 'HTTPS' == self.cobraNetwork['protocol'] or \
                    'https' == self.cobraNetwork['protocol']:
                return 'HTTPS'
            elif 'WS' == self.cobraNetwork['protocol'] or \
                    'ws' == self.cobraNetwork['protocol']:
                return 'WS'
            elif 'ICP' == self.cobraNetwork['protocol'] or \
                    'icp' == self.cobraNetwork['protocol']:
                return 'ICP'
            else:
                return 'HTTP'

    # Protocol HTTP, WS or ICP
    def get_url_host_port(self):
        if self.cobraNetwork['host'] and self.cobraNetwork['port']:
            return str(self.cobraNetwork['host']) + ':' + str(self.cobraNetwork['port'])
        if self.cobraNetwork['url']:
            if self.cobraNetwork['port']:
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

    # HDWallet
    def get_hdwallet(self):
        if 'hdwallet' in self.cobraNetwork:
            self.package_checker('cobra_hdwallet',
                                 'Please install Cobra HDWallet "pip install cobra-hdwallet"')
            if 'mnemonic' in self.cobraNetwork['hdwallet'] or \
                    'seed' in self.cobraNetwork['hdwallet']:
                if 'password' in self.cobraNetwork['hdwallet']:
                    if 'mnemonic' in self.cobraNetwork['hdwallet']:
                        return dict(
                            mnemonic=self.cobraNetwork['hdwallet']['mnemonic'],
                            password=self.cobraNetwork['hdwallet']['password']
                        )
                    elif 'seed' in self.cobraNetwork['hdwallet']:
                        return dict(
                            mnemonic=self.cobraNetwork['hdwallet']['seed'],
                            password=self.cobraNetwork['hdwallet']['password']
                        )
                else:
                    if 'mnemonic' in self.cobraNetwork['hdwallet']:
                        return dict(
                            mnemonic=self.cobraNetwork['hdwallet']['mnemonic']
                        )
                    elif 'seed' in self.cobraNetwork['hdwallet']:
                        return dict(
                            mnemonic=self.cobraNetwork['hdwallet']['seed']
                        )
            elif 'private' in self.cobraNetwork['hdwallet']:
                return dict(
                    private=self.cobraNetwork['hdwallet']['private']
                )

    # Host/Url
    def network(self):

        if self.get_protocol():


        if 'host' in self.cobraNetwork and \
                'port' in self.cobraNetwork:
            if not self.host.startswith("http://") or not self.host.startswith("https://"):
                self.host = "http://" + str(self.host)
            httpProvider = HTTPProvider(self.host + ":" + str(self.port))
            Web3Instance = Web3(httpProvider)
        elif 'url' in self.cobraNetwork:
            if 'port' in self.cobraNetwork:
                pass
            else:
                pass
