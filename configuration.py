from lazyme.string import color_print
import json
import yaml
import sys


class CobraConfiguration:

    def __init__(self):
        pass

    def cobra_print(self, text, color=None, bold=False, background=None, underline=False):
        if color == 'success':
            return color_print(text, color='green', bold=bold, highlighter=background, underline=underline)
        elif color == 'warning':
            return color_print(text, color='yellow', bold=bold, highlighter=background, underline=underline)
        elif color == 'error':
            return color_print(text, color='red', bold=bold, highlighter=background, underline=underline)
        else:
            return color_print(text, bold=bold, highlighter=background, underline=underline)

    def file_reader(self, file):
        try:
            with open(file, 'r') as read_file:
                return_file = read_file.read()
                read_file.close()
                return return_file
        except FileNotFoundError:
            self.cobra_print("[Cobra] FileNotFound: %s" % file, "error", bold=True)
        sys.exit()

    def yaml_loader(self, yaml_file):
        try:
            load_compile = yaml.load(yaml_file)
            return load_compile
        except yaml.scanner.ScannerError as scannerError:
            self.cobra_print("[Cobra] YAMLScannerError: %s" % scannerError, "error", bold=True)
        sys.exit()

    def json_loader(self, json_file):
        try:
            loaded_json = json.loads(json_file)
            return loaded_json
        except json.decoder.JSONDecodeError as jsonDecodeError:
            self.cobra_print("[Cobra] JSONDecodeError: %s" % jsonDecodeError, "error", bold=True)
        sys.exit()

    def compile(self, compile_yaml):
        compiles = []
        try:
            if compile_yaml['solidity_path_dir'] and compile_yaml['contracts']:
                artifact_path_dir = None
                try:
                    if compile_yaml['artifact_path_dir']:
                        artifact_path_dir = compile_yaml['artifact_path_dir']
                except KeyError:
                    self.cobra_print("[WARNING] Cobra: Can't find artifact_path_dir. "
                                     "By default ./build/contracts", "warning", bold=True)
                for contract in compile_yaml['contracts']:
                    try:
                        if contract['contract']['solidity']:
                            try:
                                if contract['contract']['links_path_dir']:
                                    try:
                                        if contract['contract']['solidity_path_dir']:
                                            try:
                                                if contract['contract']['remappings']:
                                                    compiles.append(dict(
                                                        solidity_path_dir=contract['contract']['solidity_path_dir'],
                                                        solidity=contract['contract']['solidity'],
                                                        links_path_dir=contract['contract']['links_path_dir'],
                                                        artifact_path_dir=artifact_path_dir,
                                                        remappings=contract['contract']['remappings']
                                                    ))
                                                    continue
                                                elif not contract['contract']['remappings']:
                                                    compiles.append(dict(
                                                        solidity_path_dir=contract['contract']['solidity_path_dir'],
                                                        solidity=contract['contract']['solidity'],
                                                        links_path_dir=contract['contract']['links_path_dir'],
                                                        artifact_path_dir=artifact_path_dir,
                                                        remappings=None
                                                    ))
                                                    continue
                                            except KeyError:
                                                compiles.append(dict(
                                                    solidity_path_dir=contract['contract']['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=contract['contract']['links_path_dir'],
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=None
                                                ))
                                                continue
                                        elif not contract['contract']['solidity_path_dir']:
                                            try:
                                                if contract['contract']['remappings']:
                                                    compiles.append(dict(
                                                        solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                        solidity=contract['contract']['solidity'],
                                                        links_path_dir=contract['contract']['links_path_dir'],
                                                        artifact_path_dir=artifact_path_dir,
                                                        remappings=contract['contract']['remappings']
                                                    ))
                                                    continue
                                                elif not contract['contract']['remappings']:
                                                    compiles.append(dict(
                                                        solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                        solidity=contract['contract']['solidity'],
                                                        links_path_dir=contract['contract']['links_path_dir'],
                                                        artifact_path_dir=artifact_path_dir,
                                                        remappings=None
                                                    ))
                                                    continue
                                            except KeyError:
                                                compiles.append(dict(
                                                    solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=contract['contract']['links_path_dir'],
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=None
                                                ))
                                                continue
                                    except KeyError:
                                        try:
                                            if contract['contract']['remappings']:
                                                compiles.append(dict(
                                                    solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=contract['contract']['links_path_dir'],
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=contract['contract']['remappings']
                                                ))
                                                continue
                                            elif not contract['contract']['remappings']:
                                                compiles.append(dict(
                                                    solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=contract['contract']['links_path_dir'],
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=None
                                                ))
                                                continue
                                        except KeyError:
                                            compiles.append(dict(
                                                solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                solidity=contract['contract']['solidity'],
                                                links_path_dir=contract['contract']['links_path_dir'],
                                                artifact_path_dir=artifact_path_dir,
                                                remappings=None
                                            ))
                                            continue
                                elif not contract['contract']['links_path_dir']:
                                    try:
                                        if contract['contract']['solidity_path_dir']:
                                            try:
                                                if contract['contract']['remappings']:
                                                    compiles.append(dict(
                                                        solidity_path_dir=contract['contract']['solidity_path_dir'],
                                                        solidity=contract['contract']['solidity'],
                                                        links_path_dir=None,
                                                        artifact_path_dir=artifact_path_dir,
                                                        remappings=contract['contract']['remappings']
                                                    ))
                                                    continue
                                                elif not contract['contract']['remappings']:
                                                    compiles.append(dict(
                                                        solidity_path_dir=contract['contract']['solidity_path_dir'],
                                                        solidity=contract['contract']['solidity'],
                                                        links_path_dir=None,
                                                        artifact_path_dir=artifact_path_dir,
                                                        remappings=None
                                                    ))
                                                    continue
                                            except KeyError:
                                                compiles.append(dict(
                                                    solidity_path_dir=contract['contract']['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=None,
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=None
                                                ))
                                                continue
                                        elif not contract['contract']['solidity_path_dir']:
                                            try:
                                                if contract['contract']['remappings']:
                                                    compiles.append(dict(
                                                        solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                        solidity=contract['contract']['solidity'],
                                                        links_path_dir=None,
                                                        artifact_path_dir=artifact_path_dir,
                                                        remappings=contract['contract']['remappings']
                                                    ))
                                                    continue
                                                elif not contract['contract']['remappings']:
                                                    compiles.append(dict(
                                                        solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                        solidity=contract['contract']['solidity'],
                                                        links_path_dir=None,
                                                        artifact_path_dir=artifact_path_dir,
                                                        remappings=None
                                                    ))
                                                    continue
                                            except KeyError:
                                                compiles.append(dict(
                                                    solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=None,
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=None
                                                ))
                                                continue
                                    except KeyError:
                                        try:
                                            if contract['contract']['remappings']:
                                                compiles.append(dict(
                                                    solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=None,
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=contract['contract']['remappings']
                                                ))
                                                continue
                                            elif not contract['contract']['remappings']:
                                                compiles.append(dict(
                                                    solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=None,
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=None
                                                ))
                                                continue
                                        except KeyError:
                                            compiles.append(dict(
                                                solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                solidity=contract['contract']['solidity'],
                                                links_path_dir=None,
                                                artifact_path_dir=artifact_path_dir,
                                                remappings=None
                                            ))
                                            continue
                            except KeyError:
                                try:
                                    if contract['contract']['solidity_path_dir']:
                                        try:
                                            if contract['contract']['remappings']:
                                                compiles.append(dict(
                                                    solidity_path_dir=contract['contract']['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=None,
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=contract['contract']['remappings']
                                                ))
                                                continue
                                            elif not contract['contract']['remappings']:
                                                compiles.append(dict(
                                                    solidity_path_dir=contract['contract']['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=None,
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=None
                                                ))
                                                continue
                                        except KeyError:
                                            compiles.append(dict(
                                                solidity_path_dir=contract['contract']['solidity_path_dir'],
                                                solidity=contract['contract']['solidity'],
                                                links_path_dir=None,
                                                artifact_path_dir=artifact_path_dir,
                                                remappings=None
                                            ))
                                            continue
                                    elif not contract['contract']['solidity_path_dir']:
                                        try:
                                            if contract['contract']['remappings']:
                                                compiles.append(dict(
                                                    solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=None,
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=contract['contract']['remappings']
                                                ))
                                                continue
                                            elif not contract['contract']['remappings']:
                                                compiles.append(dict(
                                                    solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                    solidity=contract['contract']['solidity'],
                                                    links_path_dir=None,
                                                    artifact_path_dir=artifact_path_dir,
                                                    remappings=None
                                                ))
                                                continue
                                        except KeyError:
                                            compiles.append(dict(
                                                solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                solidity=contract['contract']['solidity'],
                                                links_path_dir=None,
                                                artifact_path_dir=artifact_path_dir,
                                                remappings=None
                                            ))
                                            continue
                                except KeyError:
                                    try:
                                        if contract['contract']['remappings']:
                                            compiles.append(dict(
                                                solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                solidity=contract['contract']['solidity'],
                                                links_path_dir=None,
                                                artifact_path_dir=artifact_path_dir,
                                                remappings=contract['contract']['remappings']
                                            ))
                                            continue
                                        elif not contract['contract']['remappings']:
                                            compiles.append(dict(
                                                solidity_path_dir=compile_yaml['solidity_path_dir'],
                                                solidity=contract['contract']['solidity'],
                                                links_path_dir=None,
                                                artifact_path_dir=artifact_path_dir,
                                                remappings=None
                                            ))
                                            continue
                                    except KeyError:
                                        compiles.append(dict(
                                            solidity_path_dir=compile_yaml['solidity_path_dir'],
                                            solidity=contract['contract']['solidity'],
                                            links_path_dir=None,
                                            artifact_path_dir=artifact_path_dir,
                                            remappings=None
                                        ))
                                        continue
                    except KeyError:
                        self.cobra_print("[ERROR] Cobra: There is no solidity in contract.", "error", bold=True)
                        sys.exit()
        except KeyError:
            self.cobra_print("[ERROR] Cobra: Can't find solidity_path_dir or contracts in compile [cobra.yaml]", "error", bold=True)
            sys.exit()
        return compiles

    def deploy(self, deploy_yaml):
        deploys = []
        try:
            if deploy_yaml['artifact_path_dir'] and deploy_yaml['contracts']:
                for contract in deploy_yaml['contracts']:
                    try:
                        if contract['contract']['artifact']:
                            try:
                                if contract['contract']['links']:
                                    deploys.append(dict(
                                        artifact_path_dir=deploy_yaml['artifact_path_dir'],
                                        artifact=contract['contract']['artifact'],
                                        links=contract['contract']['links']
                                    ))
                                elif not contract['contract']['links']:
                                    deploys.append(dict(
                                        artifact_path_dir=deploy_yaml['artifact_path_dir'],
                                        artifact=contract['contract']['artifact'],
                                        links=None
                                    ))
                                    continue
                            except KeyError:
                                deploys.append(dict(
                                    artifact_path_dir=deploy_yaml['artifact_path_dir'],
                                    artifact=contract['contract']['artifact'],
                                    links=None
                                ))
                    except KeyError:
                        self.cobra_print("[ERROR] Cobra: There is no artifact in contract.", "error", bold=True)
                        sys.exit()
        except KeyError:
            self.cobra_print("[ERROR] Cobra: Can't find artifact_path_dir or contracts in deploy [cobra.yaml]", "error", bold=True)
            sys.exit()
        return deploys




