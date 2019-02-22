from lazyme.string import color_print
from solc import compile_source
from datetime import datetime
from json import loads, dumps
from os.path import basename
import json
import web3
import sys
import re
import os


class CobraCompile:

    network = """{,\n "networks": {},\n "updatedAt": "%s"\n}""" % str(datetime.now())

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

    def strip(self, strip):
        return strip.strip()[1:-1]

    def file_reader(self, file_path):
        try:
            with open(file_path, 'r') as read_file:
                return_file = read_file.read()
                read_file.close()
                return return_file
        except FileNotFoundError:
            self.cobra_print("[ERROR] Cobra-FileNotFound: %s" % file_path, "error", bold=True)
            sys.exit()

    def file_writer(self, file_path, docs):
        with open(file_path, 'w') as write_file:
            write_file.write(docs)
            write_file.close()
            return

    def bytecode_link_to_md5(self, bytecode, contract_interface):
        count = 0
        contract_bytecode = []
        split_bytecode = re.split('__+', bytecode)
        files = self.bytecode_link_from_file(contract_interface)
        for index, contract in enumerate(split_bytecode):
            if len(contract) < 40 and (index % 2) != 0:
                underscore = "_"
                link_bytecode = 40
                file = "__" + str(files[count])
                length_of_file = len(file)
                contract_name = file + ((link_bytecode - length_of_file) * underscore)
                contract_bytecode.append(contract_name)
                count = count + 1
            else:
                contract_bytecode.append(contract)
        return "".join(contract_bytecode)

    def bytecode_link_from_file(self, contract_interface):
        files = []
        children = contract_interface['ast']['children']
        for attributes in children:
            try:
                file = attributes['attributes']['file']
                files.append(basename(file)[:-4])
            except KeyError:
                continue
        return files



