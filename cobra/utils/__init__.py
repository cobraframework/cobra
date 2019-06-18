from .console_log import console_log
import json, yaml, sys


def file_reader(file_path):
    try:
        with open(file_path, 'r') as read_file:
            return_file = read_file.read()
            read_file.close()
            return return_file
    except FileNotFoundError:
        console_log("No such file or directory '%s'" % file_path,
                    "error", "FileNotFoundError")
    sys.exit()


def yaml_loader(yaml_file, more=False):
    try:
        load_compile = yaml.load(yaml_file)
        return load_compile
    except yaml.scanner.ScannerError as scannerError:
        if more:
            console_log(str(scannerError),
                        "error", "ScannerError")
        else:
            console_log(str(scannerError).split('\n')[0],
                        "error", "ScannerError")
    except yaml.parser.ParserError as parserError:
        if more:
            console_log(str(parserError),
                        "error", "ParserError")
        else:
            console_log(str(parserError).split('\n')[0],
                        "error", "ParserError")
    sys.exit()


def json_loader(json_file, more=False):
    try:
        loaded_json = json.loads(json_file)
        return loaded_json
    except json.decoder.JSONDecodeError as jsonDecodeError:
        if more:
            console_log(str(jsonDecodeError),
                        "error", "JSONDecodeError")
        else:
            console_log(str(jsonDecodeError).split('\n')[0],
                        "error", "JSONDecodeError")
    sys.exit()
