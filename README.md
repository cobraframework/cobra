<img src="../master/cobra.png?raw=true" width="225">

![GitHub License](https://img.shields.io/github/license/cobraframework/pytest-cobra.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)
![PyPI Version](https://img.shields.io/pypi/v/pytest-cobra.svg)
![Github Date](https://img.shields.io/github/release-date/cobraframework/pytest-cobra.svg?color=black)
![PyPI Wheel](https://img.shields.io/pypi/wheel/pytest-cobra.svg)
[![Donate with Ethereum](https://en.cryptobadges.io/badge/micro/0xD32AAEDF28A848e21040B6F643861A9077F83106)](https://en.cryptobadges.io/donate/0xD32AAEDF28A848e21040B6F643861A9077F83106)

---

*A fast, flexible and simple development environment framework for Ethereum smart contract, testing and 
deployment on Ethereum virtual machine(EVM).*

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

## Testing
Tests are still under development.

You can run the tests with:
```
$ pytest tests
```

## Meta

**Meheret Tesfaye** – [@meherett](https://github.com/meherett) – meherett@zoho.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/meherett](https://github.com/meherett)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

