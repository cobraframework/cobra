from colorama import Fore, Style
import json
import yaml
import sys


class CobraConfiguration:

    def __init__(self):
        pass

    def cobra_print(self, text, type=None, title=None, space=False, space_number=0):
        # Checking text instance is string
        if isinstance(text, str):
            if title is None:
                if type == 'success':
                    return print(Style.DIM + Fore.GREEN + '[SUCCESS]'
                                 + Style.RESET_ALL + ' ' + text)
                elif type == 'warning':
                    return print(Style.DIM + Fore.YELLOW + '[WARNING]'
                                 + Style.RESET_ALL + ' ' + text)
                elif type == 'error':
                    return print(Style.DIM + Fore.RED + '[ERROR]'
                                 + Style.RESET_ALL + ' ' + text)
                else:
                    return print(text)
            elif title is not None \
                    and isinstance(title, str) and not space:
                if type == 'success':
                    return print(Style.DIM + Fore.GREEN + '[SUCCESS]'
                                 + Style.RESET_ALL + ' ' + Fore.WHITE + title
                                 + ': ' + Style.RESET_ALL + text)
                elif type == 'warning':
                    return print(Style.DIM + Fore.YELLOW + '[WARNING]'
                                 + Style.RESET_ALL + ' ' + Fore.WHITE + title
                                 + ': ' + Style.RESET_ALL + text)
                elif type == 'error':
                    return print(Style.DIM + Fore.RED + '[ERROR]'
                                 + Style.RESET_ALL + ' ' + Fore.WHITE + title
                                 + ': ' + Style.RESET_ALL + text)
                else:
                    return print(Fore.WHITE + title
                                 + ': ' + Style.RESET_ALL + text)
            elif title is not None \
                    and isinstance(title, str) and space:
                if type == 'success':
                    return print(Style.DIM + Fore.GREEN + '         '
                                 + Style.RESET_ALL + ' ' + Fore.WHITE + title
                                 + ': ' + Style.RESET_ALL + text)
                elif type == 'warning':
                    return print(Style.DIM + Fore.YELLOW + '         '
                                 + Style.RESET_ALL + ' ' + Fore.WHITE + title
                                 + ': ' + Style.RESET_ALL + text)
                elif type == 'error':
                    return print(Style.DIM + Fore.RED + '      '
                                 + Style.RESET_ALL + ' ' + Fore.WHITE + title
                                 + ': ' + Style.RESET_ALL + text)
                else:
                    if space_number is 0:
                        return print(Fore.WHITE + '' + title
                                     + ': ' + Style.RESET_ALL + text)
                    else:
                        return print(Fore.WHITE + ' ' * space_number + title
                                     + ': ' + Style.RESET_ALL + text)

    def fileReader(self, file_path):
        try:
            with open(file_path, 'r') as read_file:
                return_file = read_file.read()
                read_file.close()
                return return_file
        except FileNotFoundError:
            self.cobra_print("No such file or directory '%s'" % file_path,
                             "error", "FileNotFoundError")
        sys.exit()

    def yamlLoader(self, yaml_file, more=False):
        try:
            load_compile = yaml.load(yaml_file)
            return load_compile
        except yaml.scanner.ScannerError as scannerError:
            if more:
                self.cobra_print(str(scannerError),
                                 "error", "ScannerError")
            else:
                self.cobra_print(str(scannerError).split('\n')[0],
                                 "error", "ScannerError")
        except yaml.parser.ParserError as parserError:
            if more:
                self.cobra_print(str(parserError),
                                 "error", "ParserError")
            else:
                self.cobra_print(str(parserError).split('\n')[0],
                                 "error", "ParserError")
        sys.exit()

    def jsonLoader(self, json_file, more=False):
        try:
            loaded_json = json.loads(json_file)
            return loaded_json
        except json.decoder.JSONDecodeError as jsonDecodeError:
            if more:
                self.cobra_print(str(jsonDecodeError),
                                 "error", "JSONDecodeError")
            else:
                self.cobra_print(str(jsonDecodeError).split('\n')[0],
                                 "error", "JSONDecodeError")
        sys.exit()

    def hasRemapping(self, contract):
        # Finding import_remappings and checking not None
        if 'import_remappings' in contract and \
                contract['import_remappings']:
            return True
        # Finding import_remappings and checking None
        elif 'import_remappings' in contract and \
                not contract['import_remappings']:
            return False
        else:
            return False

    def hasSolidityPathDir(self, contract):
        # Finding solidity path dir and checking not None
        if 'solidity_path_dir' in contract and \
                contract['solidity_path_dir']:
            return True
        # Finding solidity path dir and checking None
        elif 'solidity_path_dir' in contract and \
                not contract['solidity_path_dir']:
            return False
        else:
            return False

    def hasLinksPathDir(self, contract):
        # Finding links path dir on contract checking not None
        if 'allow_paths' in contract and \
                contract['allow_paths']:
            return True
        # Finding links path dir on contract checking None
        elif 'allow_paths' in contract and \
                not contract['allow_paths']:
            return False
        else:
            return False

    def compile(self, compile_yaml):
        compiles = []

        # Finding solidity path directory
        if 'solidity_path_dir' in compile_yaml:
            # Finding contracts array
            if 'contracts' in compile_yaml:
                # Checking artifact path directory
                if 'artifact_path_dir' in compile_yaml:
                    artifact_path_dir = compile_yaml['artifact_path_dir']
                else:
                    artifact_path_dir = "./build/contracts"
                    self.cobra_print("artifact_path_dir on compile. "
                                     "by default uses './build/contracts'", "warning", "NotFound")
                # Looping contracts
                for contract in compile_yaml['contracts']:
                    # Finding solidity on contract
                    if 'contract' in contract:
                        if 'solidity' in contract['contract']:
                            if self.hasLinksPathDir(contract['contract']):
                                if self.hasSolidityPathDir(contract['contract']):
                                    if self.hasRemapping(contract['contract']):
                                        compiles.append(dict(
                                            solidity_path_dir=contract['contract']['solidity_path_dir'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=contract['contract']['allow_paths'],
                                            artifact_path_dir=artifact_path_dir,
                                            import_remappings=contract['contract']['import_remappings']
                                        ))
                                        continue
                                    else:
                                        compiles.append(dict(
                                            solidity_path_dir=contract['contract']['solidity_path_dir'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=contract['contract']['allow_paths'],
                                            artifact_path_dir=artifact_path_dir,
                                            import_remappings=None
                                        ))
                                        continue
                                else:
                                    if self.hasRemapping(contract['contract']):
                                        compiles.append(dict(
                                            solidity_path_dir=compile_yaml['solidity_path_dir'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=contract['contract']['allow_paths'],
                                            artifact_path_dir=artifact_path_dir,
                                            import_remappings=contract['contract']['import_remappings']
                                        ))
                                        continue
                                    else:
                                        compiles.append(dict(
                                            solidity_path_dir=compile_yaml['solidity_path_dir'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=contract['contract']['allow_paths'],
                                            artifact_path_dir=artifact_path_dir,
                                            import_remappings=None
                                        ))
                                        continue
                            else:
                                if self.hasSolidityPathDir(contract['contract']):
                                    if self.hasRemapping(contract['contract']):
                                        compiles.append(dict(
                                            solidity_path_dir=contract['contract']['solidity_path_dir'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=None,
                                            artifact_path_dir=artifact_path_dir,
                                            import_remappings=contract['contract']['import_remappings']
                                        ))
                                        continue
                                    else:
                                        compiles.append(dict(
                                            solidity_path_dir=contract['contract']['solidity_path_dir'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=None,
                                            artifact_path_dir=artifact_path_dir,
                                            import_remappings=None
                                        ))
                                        continue
                                else:
                                    if self.hasRemapping(contract['contract']):
                                        compiles.append(dict(
                                            solidity_path_dir=compile_yaml['solidity_path_dir'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=None,
                                            artifact_path_dir=artifact_path_dir,
                                            import_remappings=contract['contract']['import_remappings']
                                        ))
                                        continue
                                    else:
                                        compiles.append(dict(
                                            solidity_path_dir=compile_yaml['solidity_path_dir'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=None,
                                            artifact_path_dir=artifact_path_dir,
                                            import_remappings=None
                                        ))
                                        continue
                        else:
                            self.cobra_print("solidity in contract [cobra.yaml]",
                                             "error", "NotFound")
                            sys.exit()
                    else:
                        self.cobra_print("contract in contracts [cobra.yaml]",
                                         "error", "NotFound")
                        sys.exit()
            else:
                self.cobra_print("contracts in compile [cobra.yaml]",
                                 "error", "NotFound")
                sys.exit()
        else:
            self.cobra_print("solidity_path_dir in compile [cobra.yaml]",
                             "error", "NotFound")
            sys.exit()

        return compiles

    def deploy(self, deploy_yaml):
        deploys = []

        if 'artifact_path_dir' in deploy_yaml:
            if 'contracts' in deploy_yaml:
                for contract in deploy_yaml['contracts']:

                    if 'artifact' in contract['contract']:
                        if 'links' in contract['contract']:
                            if contract['contract']['links']:
                                deploys.append(dict(
                                    artifact_path_dir=deploy_yaml['artifact_path_dir'],
                                    artifact=contract['contract']['artifact'],
                                    links=contract['contract']['links']
                                ))
                                continue
                            elif not contract['contract']['links']:
                                deploys.append(dict(
                                    artifact_path_dir=deploy_yaml['artifact_path_dir'],
                                    artifact=contract['contract']['artifact'],
                                    links=None
                                ))
                                continue
                        else:
                            deploys.append(dict(
                                artifact_path_dir=deploy_yaml['artifact_path_dir'],
                                artifact=contract['contract']['artifact'],
                                links=None
                            ))
                            continue
                    else:
                        self.cobra_print("artifact in contract [cobra.yaml]",
                                         "error", "NotFound")
                        sys.exit()
            else:
                self.cobra_print("contracts in deploy [cobra.yaml]",
                                 "error", "NotFound")
                sys.exit()
        else:
            self.cobra_print("artifact_path_dir in deploy [cobra.yaml]",
                             "error", "NotFound")
            sys.exit()

        return deploys

    def test(self, test_yaml):
        tests = []

        if 'artifact_path_dir' in test_yaml:
            if 'contracts' in test_yaml:
                for contract in test_yaml['contracts']:

                    if 'artifact' in contract['contract']:
                        if 'links' in contract['contract']:
                            if contract['contract']['links']:
                                tests.append(dict(
                                    artifact_path_dir=test_yaml['artifact_path_dir'],
                                    artifact=contract['contract']['artifact'],
                                    links=contract['contract']['links']
                                ))
                                continue
                            elif not contract['contract']['links']:
                                tests.append(dict(
                                    artifact_path_dir=test_yaml['artifact_path_dir'],
                                    artifact=contract['contract']['artifact'],
                                    links=None
                                ))
                                continue
                        else:
                            tests.append(dict(
                                artifact_path_dir=test_yaml['artifact_path_dir'],
                                artifact=contract['contract']['artifact'],
                                links=None
                            ))
                            continue
                    else:
                        self.cobra_print("artifact in contract [cobra.yaml]",
                                         "error", "NotFound")
                        sys.exit()
            else:
                self.cobra_print("contracts in test [cobra.yaml]",
                                 "error", "NotFound")
                sys.exit()
        else:
            self.cobra_print("artifact_path_dir in test [cobra.yaml]",
                             "error", "NotFound")
            sys.exit()

        return tests

    def account(self, account_yaml):
        if 'address' in account_yaml:
            if 'gas' in account_yaml:
                if 'gas_price' in account_yaml:
                    return dict(account=dict(
                        address=account_yaml['address'],
                        gas=account_yaml['gas'],
                        gas_price=account_yaml['gas_price']
                    ))
                else:
                    return dict(account=dict(
                        address=account_yaml['address'],
                        gas=account_yaml['gas']
                    ))
            else:
                if 'gas_price' in account_yaml:
                    return dict(account=dict(
                        address=account_yaml['address'],
                        gas_price=account_yaml['gas_price']
                    ))
                else:
                    return dict(account=dict(
                        address=account_yaml['address']
                    ))
        elif 'gas' in account_yaml:
            if 'gas_price' in account_yaml:
                return dict(account=dict(
                    gas=account_yaml['gas'],
                    gas_price=account_yaml['gas_price']
                ))
            else:
                return dict(account=dict(
                    gas=account_yaml['gas']
                ))
        else:
            self.cobra_print("address/gas in account [cobra.yaml]", "error", "NotFound")
            sys.exit()

    def hdwallet(self, hdwallet_yaml):
        if 'mnemonic' in hdwallet_yaml or \
                'seed' in hdwallet_yaml or \
                'private' in hdwallet_yaml:
            # returns Mnemonic and Password
            if 'mnemonic' in hdwallet_yaml and 'password' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            password=hdwallet_yaml['password'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            password=hdwallet_yaml['password'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            password=hdwallet_yaml['password'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            password=hdwallet_yaml['password']
                        ))
            # returns Mnemonic
            elif 'mnemonic' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['mnemonic']
                        ))
            # returns Mnemonic (Seed is alias Mnemonic) and Password
            if 'seed' in hdwallet_yaml and 'password' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            password=hdwallet_yaml['password'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            password=hdwallet_yaml['password'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            password=hdwallet_yaml['password'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            password=hdwallet_yaml['password']
                        ))
            # returns Mnemonic (Seed is alias Mnemonic)
            elif 'seed' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            mnemonic=hdwallet_yaml['seed']
                        ))
            # returns Private Key
            if 'private' in hdwallet_yaml:
                if 'gas' in hdwallet_yaml:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            private=hdwallet_yaml['private'],
                            gas=hdwallet_yaml['gas'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            private=hdwallet_yaml['private'],
                            gas=hdwallet_yaml['gas']
                        ))
                else:
                    if 'gas_price' in hdwallet_yaml:
                        return dict(hdwallet=dict(
                            private=hdwallet_yaml['private'],
                            gas_price=hdwallet_yaml['gas_price']
                        ))
                    else:
                        return dict(hdwallet=dict(
                            private=hdwallet_yaml['private']
                        ))
        else:
            self.cobra_print("mnemonic(seed)/private in hdwallet [cobra.yaml]", "error")
            sys.exit()

    def network(self, network_yaml):
        if 'development' in network_yaml:
            if 'host' in network_yaml['development'] or \
                    'url' in network_yaml['development']:
                if 'host' in network_yaml['development']:
                    if 'port' in network_yaml['development']:
                        # Protocol
                        if 'protocol' in network_yaml['development']:

                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                        # No Protocol
                        else:
                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    host=network_yaml['development']['host'],
                                    port=network_yaml['development']['port']
                                )
                    else:
                        self.cobra_print("port in %s when you are using host."
                                         % 'development', "error", "Error")
                        sys.exit()
                elif 'url' in network_yaml['development']:
                    # Port
                    if 'port' in network_yaml['development']:
                        # Protocol
                        if 'protocol' in network_yaml['development']:

                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port'],
                                    protocol=network_yaml['development']['protocol']
                                )
                        # No Protocol
                        else:
                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    url=network_yaml['development']['url'],
                                    port=network_yaml['development']['port']
                                )
                    # No Port
                    else:
                        # Protocol
                        if 'protocol' in network_yaml['development']:

                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url'],
                                    protocol=network_yaml['development']['protocol']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    url=network_yaml['development']['url'],
                                    protocol=network_yaml['development']['protocol']
                                )
                        # No Protocol
                        else:
                            if 'hdwallet' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url']
                                )
                                hdwallet = self.hdwallet(network_yaml['development']['hdwallet'])
                                return {**__, **hdwallet}
                            elif 'account' in network_yaml['development']:
                                __ = dict(
                                    url=network_yaml['development']['url']
                                )
                                account = self.account(network_yaml['development']['account'])
                                return {**__, **account}
                            else:
                                return dict(
                                    url=network_yaml['development']['url']
                                )
            else:
                self.cobra_print("host/url in %s [cobra.yaml]" % 'development',
                                 "error", "NotFound")
                sys.exit()
        else:
            self.cobra_print("development in network [cobra.yaml]",
                             "error", "NotFound")
            sys.exit()
