from cobra.utils.console_log import console_log
import sys


class CobraConfiguration:

    def __init__(self):
        pass

    @staticmethod
    def import_remapping(contract):
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

    @staticmethod
    def solidity_path(contract):
        # Finding solidity path dir and checking not None
        if 'solidity_path' in contract and \
                contract['solidity_path']:
            return True
        # Finding solidity path dir and checking None
        elif 'solidity_path' in contract and \
                not contract['solidity_path']:
            return False
        else:
            return False

    @staticmethod
    def allow_paths(contract):
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
        if 'solidity_path' in compile_yaml:
            # Finding contracts array
            if 'contracts' in compile_yaml:
                # Checking artifact path directory
                if 'artifact_path' in compile_yaml:
                    artifact_path = compile_yaml['artifact_path']
                else:
                    artifact_path = "./build/contracts"
                    console_log("artifact_path on compile. "
                                "by default uses './build/contracts'", "warning", "NotFound")
                # Looping contracts
                for contract in compile_yaml['contracts']:
                    # Finding solidity on contract
                    if 'contract' in contract:
                        if 'solidity' in contract['contract']:
                            if self.allow_paths(contract['contract']):
                                if self.solidity_path(contract['contract']):
                                    if self.import_remapping(contract['contract']):
                                        compiles.append(dict(
                                            solidity_path=contract['contract']['solidity_path'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=contract['contract']['allow_paths'],
                                            artifact_path=artifact_path,
                                            import_remappings=contract['contract']['import_remappings']
                                        ))
                                        continue
                                    else:
                                        compiles.append(dict(
                                            solidity_path=contract['contract']['solidity_path'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=contract['contract']['allow_paths'],
                                            artifact_path=artifact_path,
                                            import_remappings=None
                                        ))
                                        continue
                                else:
                                    if self.import_remapping(contract['contract']):
                                        compiles.append(dict(
                                            solidity_path=compile_yaml['solidity_path'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=contract['contract']['allow_paths'],
                                            artifact_path=artifact_path,
                                            import_remappings=contract['contract']['import_remappings']
                                        ))
                                        continue
                                    else:
                                        compiles.append(dict(
                                            solidity_path=compile_yaml['solidity_path'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=contract['contract']['allow_paths'],
                                            artifact_path=artifact_path,
                                            import_remappings=None
                                        ))
                                        continue
                            else:
                                if self.solidity_path(contract['contract']):
                                    if self.import_remapping(contract['contract']):
                                        compiles.append(dict(
                                            solidity_path=contract['contract']['solidity_path'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=None,
                                            artifact_path=artifact_path,
                                            import_remappings=contract['contract']['import_remappings']
                                        ))
                                        continue
                                    else:
                                        compiles.append(dict(
                                            solidity_path=contract['contract']['solidity_path'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=None,
                                            artifact_path=artifact_path,
                                            import_remappings=None
                                        ))
                                        continue
                                else:
                                    if self.import_remapping(contract['contract']):
                                        compiles.append(dict(
                                            solidity_path=compile_yaml['solidity_path'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=None,
                                            artifact_path=artifact_path,
                                            import_remappings=contract['contract']['import_remappings']
                                        ))
                                        continue
                                    else:
                                        compiles.append(dict(
                                            solidity_path=compile_yaml['solidity_path'],
                                            solidity=contract['contract']['solidity'],
                                            allow_paths=None,
                                            artifact_path=artifact_path,
                                            import_remappings=None
                                        ))
                                        continue
                        else:
                            console_log("solidity in contract [cobra.yaml]",
                                        "error", "NotFound")
                            sys.exit()
                    else:
                        console_log("contract in contracts [cobra.yaml]",
                                    "error", "NotFound")
                        sys.exit()
            else:
                console_log("contracts in compile [cobra.yaml]",
                            "error", "NotFound")
                sys.exit()
        else:
            console_log("solidity_path in compile [cobra.yaml]",
                        "error", "NotFound")
            sys.exit()

        return compiles

    @staticmethod
    def deploy(deploy_yaml):
        deploys = []

        if 'artifact_path' in deploy_yaml:
            if 'contracts' in deploy_yaml:
                for contract in deploy_yaml['contracts']:

                    if 'artifact' in contract['contract']:
                        if 'links' in contract['contract']:
                            if contract['contract']['links']:
                                deploys.append(dict(
                                    artifact_path=deploy_yaml['artifact_path'],
                                    artifact=contract['contract']['artifact'],
                                    links=contract['contract']['links']
                                ))
                                continue
                            elif not contract['contract']['links']:
                                deploys.append(dict(
                                    artifact_path=deploy_yaml['artifact_path'],
                                    artifact=contract['contract']['artifact'],
                                    links=None
                                ))
                                continue
                        else:
                            deploys.append(dict(
                                artifact_path=deploy_yaml['artifact_path'],
                                artifact=contract['contract']['artifact'],
                                links=None
                            ))
                            continue
                    else:
                        console_log("artifact in contract [cobra.yaml]",
                                    "error", "NotFound")
                        sys.exit()
            else:
                console_log("contracts in deploy [cobra.yaml]",
                            "error", "NotFound")
                sys.exit()
        else:
            console_log("artifact_path in deploy [cobra.yaml]",
                        "error", "NotFound")
            sys.exit()

        return deploys

    @staticmethod
    def test(test_yaml):
        tests = []

        if 'artifact_path' in test_yaml:
            if 'contracts' in test_yaml:
                for contract in test_yaml['contracts']:

                    if 'artifact' in contract['contract']:
                        if 'links' in contract['contract']:
                            if contract['contract']['links']:
                                tests.append(dict(
                                    artifact_path=test_yaml['artifact_path'],
                                    artifact=contract['contract']['artifact'],
                                    links=contract['contract']['links']
                                ))
                                continue
                            elif not contract['contract']['links']:
                                tests.append(dict(
                                    artifact_path=test_yaml['artifact_path'],
                                    artifact=contract['contract']['artifact'],
                                    links=None
                                ))
                                continue
                        else:
                            tests.append(dict(
                                artifact_path=test_yaml['artifact_path'],
                                artifact=contract['contract']['artifact'],
                                links=None
                            ))
                            continue
                    else:
                        console_log("artifact in contract [cobra.yaml]",
                                    "error", "NotFound")
                        sys.exit()
            else:
                console_log("contracts in test [cobra.yaml]",
                            "error", "NotFound")
                sys.exit()
        else:
            console_log("artifact_path in test [cobra.yaml]",
                        "error", "NotFound")
            sys.exit()

        return tests

    @staticmethod
    def account(account_yaml):
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
            console_log("address/gas in account [cobra.yaml]", "error", "NotFound")
            sys.exit()

    @staticmethod
    def hdwallet(hdwallet_yaml):
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
            console_log("mnemonic(seed)/private in hdwallet [cobra.yaml]", "error")
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
                        console_log("port in %s when you are using host."
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
                console_log("host/url in %s [cobra.yaml]" % 'development',
                            "error", "NotFound")
                sys.exit()
        else:
            console_log("development in network [cobra.yaml]",
                        "error", "NotFound")
            sys.exit()
