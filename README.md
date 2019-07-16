<img src="https://raw.githubusercontent.com/cobraframework/cobra/master/cobra.png" width="225">

[![Build Status](https://travis-ci.com/cobraframework/cobra.svg?branch=master)](https://travis-ci.com/cobraframework/cobra)
![PyPI Python Version](https://img.shields.io/pypi/pyversions/eth-cobra.svg)
![PyPI License](https://img.shields.io/pypi/l/eth-cobra.svg?color=black)
![PyPI Version](https://img.shields.io/pypi/v/eth-cobra.svg?color=blue)
[![Coverage Status](https://coveralls.io/repos/github/cobraframework/cobra/badge.svg?branch=master)](https://coveralls.io/github/cobraframework/cobra?branch=master)

---

A fast, flexible and simple development environment framework for Ethereum smart contract, testing and 
deployment on Ethereum virtual machine(EVM).

With cobra you can get built-in smart contract compilation, linking, deployment, binary management, 
automated contract testing with Unittest and PyTest frameworks, scriptable deployment & migrations framework 
and network management for deploying to many public & private networks like [INFURA](https://infura.io) or 
[Ganache CLI](https://github.com/trufflesuite/ganache-cli).

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
pip install eth-cobra
```

## Development
We welcome pull requests. To get started, just fork this repo, clone it locally, and run:
```
pip install -e . -r requirements.txt
```

## Quick Usage

Initialize project structure 

A default set of contract and tests, run the following command: 

```
cobra init
```

Get help:

```
cobra --help
```

From there, you can run `cobra compile`, `cobra deploy/migrate` and `cobra test --unittest/--pytest` 
to compile your contracts, deploy those contracts to the network, and run their associated unit tests.
 
 
<details>
<summary>advanced cobra.yaml</summary>

```yaml
compile:
  solidity_path: "./contracts" # global
  artifact_path: "./build/contracts"
  contracts: [
    contract: {
        solidity: "Contract.sol",
        solidity_path: "./contracts/libs", # detail
        import_remappings: [
          "=/path/folder/contracts/"
       ],
        allow_paths: [
          "/path/folder/contracts/"
        ]
    }
  ]

deploy:
  artifact_path: "./build/contracts/"
  contracts: [
    contract: {
        artifact: "Contract.json",
        links: ["Contract.json"]
    }
  ]

test:
  artifact_path: "./build/contracts/"
  test_paths: ["./tests"]
  contracts: [
    contract: {
        artifact: "Contract.json",
        links: ["Contract.json"]
    }
  ]

network:
  development: {
    url: "https://ropsten.infura.io/...",
    host: "localhost",
    port: 8545,
    hdwallet: {
        mnemonic: "decide adjust legend nation type same task aim rigid lucky guilt close", # or
        seed: "decide adjust legend nation type same task aim rigid lucky guilt close",
        password: "meherett",
        private: "5f8935bb3b61b312ba1114cbf6f1ea30102383f2b043a1b213aa482132d25049",
        gas: 3000000,
        gas_price: 1000000
    },
    protocol: "HTTP", # HTTP, HTTPS, WS(WebSocket) and ICP
    account: {
      address: "0x6a373a75c388ac2d160f1d2b6d9ada34f29831cd",
      gas: 3000000,
      gas_price: 1000000
    }
  }
```
</details>

## Testing
Tests are still under development.

You can run the tests with:

```
pytest tests
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

## Meta

Meheret Tesfaye – [@meherett](https://github.com/meherett) – meherett@zoho.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/meherett](https://github.com/meherett)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

