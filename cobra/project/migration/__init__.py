import json
import requests
import random
import sys
import websockets

from json import loads, dumps
from solc import link_code
from os.path import join
from datetime import datetime
from web3 import Web3

from cobra.utils import (
    file_reader,
    json_loader,
    yaml_loader,
    generate_numbers,
    file_writer
)
from cobra.project.provider import Provider
from cobra.utils.console_log import console_log


network = """{,
     "network": {},
     "updatedAt": "%s"
    }""" % str(datetime.now())


__all__ = [
    "Web3",
    "loads",
    "dumps",
    "json",
    "network",
    "link_code",
    "Provider",
    "requests",
    "random",
    "join",
    "generate_numbers",
    "file_writer",
    "sys",
    "file_reader",
    "json_loader",
    "yaml_loader",
    "console_log",
    "websockets",
    "datetime",
]
