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








