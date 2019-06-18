import json
import solc
import sys
import web3
import os
import re

from json import loads, dumps
from os.path import basename
from colorama import Fore, Style
from solc import compile_source
from datetime import datetime

network = """{,\n "networks": {},\n "updatedAt": "%s"\n}""" % str(datetime.now())

__all__ = [
    "loads",
    "dumps",
    "json",
    "basename",
    "solc",
    "sys",
    "Fore",
    "Style",
    "compile_source",
    "datetime",
    "web3",
    "re",
    "os",
    "network"
]
