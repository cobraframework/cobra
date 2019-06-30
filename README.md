<img src="../master/cobra.png?raw=true" width="225">

[![Build Status](https://travis-ci.com/meherett/cobra.svg?token=zWs2UgQUy4zmDh4gtGYH&branch=master)](https://travis-ci.com/meherett/cobra)
![GitHub License](https://img.shields.io/github/license/cobraframework/pytest-cobra.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-cobra.svg)
![PyPI Version](https://img.shields.io/pypi/v/pytest-cobra.svg)
[![Donate with Ethereum](https://en.cryptobadges.io/badge/micro/0xD32AAEDF28A848e21040B6F643861A9077F83106)](https://en.cryptobadges.io/donate/0xD32AAEDF28A848e21040B6F643861A9077F83106)

---

A fast, flexible and simple development environment framework for Ethereum smart contract, testing and 
deployment on Ethereum virtual machine(EVM).

With cobra you can get built-in smart contract compilation, linking, deployment, binary management, 
automated contract testing with Unittest and PyTest frameworks, scriptable deployment & migrations framework 
and network management for deploying to many public & private networks like INFURA or ganache-cli.

## Dependency

This library requires the `solc` executable to be present.

Only versions `>=0.4.2` are supported and tested though this library may work
with other versions.

* [solc](http://solidity.readthedocs.io/en/latest/installing-solidity.html): Ethereum solidity compiler.
* [ganache-cli](https://github.com/trufflesuite/ganache-cli): A command-line version of Ethereum blockchain server.
* [pip](https://pypi.org/project/pip/): To install packages from the Python Package Index and other indexes.
* [python3](https://www.python.org/downloads/release/python-368/): version 3.6 or greater.

## Installation
PIP to install cobra globally. For Linux sudo may be required.
```
$ pip install py-cobra
```

## Development
We welcome pull requests. To get started, just fork this repo, clone it locally, and run:
```
$ pip install -e . -r requirements.txt
```

## Quick Usage

Initialize project structure 

A default set of contract and tests, run the following command: 

```
$ cobra init
```

Get help:

```
$ cobra --help
```

From there, you can run `cobra compile`, `cobra deploy/migrate` and `cobra test --unittest/--pytest` 
to compile your contracts, deploy those contracts to the network, and run their associated unit tests.

<details>
advanced <summary>cobra.yaml</summary>

```yaml
compile:
  solidity_path: "./contracts" # global solidity path location
  artifact_path: "./build/contracts"
  contracts: [
    contract: {
        solidity: "Contract.sol",
#        solidity_path: "./contracts/libs", # detail solidity path location
#        import_remappings: [
#          "=/home/meheret/PycharmProjects/metacoin-example/contracts/"
#        ],
#        allow_paths: [
#          "/home/meheret/PycharmProjects/metacoin-example/contracts/"
#        ]
    }
  ]

deploy:
  artifact_path: "./build/contracts/"
  contracts: [
    contract: {
        artifact: "Contract.json",
    #        links: ["Contract.json"]
    }
  ]

test:
  artifact_path: "./build/contracts/"
  test_paths: ["./tests"]
  contracts: [
    contract: {
        artifact: "Contract.json",
#        links: ["Contract.json"]
    }
  ]

network:
  development: {
    url: "https://ropsten.infura.io/...",
    host: "localhost",
    port: 8545,
#    hdwallet: {
#        mnemonic: "meheret tesfaye batu bayou",
#        seed: "meheret tesfaye batu bayou",
#        password: "meherett",
#        private: "5f8935bb3b61b312ba1114cbf6f1ea30102383f2b043a1b213aa482132d25049",
#        gas: 3000000,
#        gas_price: 1000000
#    },
    protocol: "HTTP", # HTTP, HTTPS, WS(WebSocket) and ICP
    account: {
      address: "0x6a373a75c388ac2d160f1d2b6d9ada34f29831cd",
      gas: 3000000,
#      gas_price: 1000000
    }
  }
```
</details>

## Testing
Tests are still under development.

You can run the tests with:

```
$ pytest tests
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

## Meta

Meheret Tesfaye – [@meherett](https://github.com/meherett) – meherett@zoho.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/meherett](https://github.com/meherett)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

