<p align="center">	
  <img src="https://raw.githubusercontent.com/Cobraframework/pytest-cobra/master/pytest-cobra.png">		
</p>

# PyTest-Cobra ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-cobra.svg?style=for-the-badge)

*PyTest plugin for testing Smart Contracts for Ethereum blockchain.*

![GitHub License](https://img.shields.io/github/license/cobraframework/pytest-cobra.svg)
![PyPI Version](https://img.shields.io/pypi/v/pytest-cobra.svg?color=blue)
![Github Date](https://img.shields.io/github/release-date/cobraframework/pytest-cobra.svg)
![PyPI Wheel](https://img.shields.io/pypi/wheel/pytest-cobra.svg?color=%2308490e)
[![Donate with Ethereum](https://en.cryptobadges.io/badge/micro/0xD32AAEDF28A848e21040B6F643861A9077F83106)](https://en.cryptobadges.io/donate/0xD32AAEDF28A848e21040B6F643861A9077F83106)

## Dependency

This library requires the `solc` executable to be present.

Only versions `>=0.4.2` are supported and tested though this library may work
with other versions.

[solc installation instructions](http://solidity.readthedocs.io/en/latest/installing-solidity.html)

Install Solidity compiler (solc) using Node Package  Manager(npm)
```
npm install -g solc
```
or for Ubuntu(Linux)
```
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc
```

## Quickstart
Installation
```
pip install pytest-cobra
```

## Development
Clone the repository and then run
```
pip install -e . -r requirements.txt
```

## Usage

#### Execute your test suite
 Example MetaCoin
 [picture](https://github.com/cobraframework/pytest-cobra/blob/master/example/example.png)

```python
# MetaCoin Testing

# cobra is pytest fixture
def test_metacoin(cobra):

    # Getting Contract Factory by name
    metacoin = cobra.contract('MetaCoin')
    
    # Getting Contract Instance of MetaCoin
    metacoin = metacoin.deploy()

    assert metacoin.getBalance(cobra.accounts[0]) == 10000
```

### Running test from Solidity file (.sol)

```
pytest --cobra MetaCoin.sol
```

#### Optional commands

##### Import path remappings
`solc` provides path aliasing allow you to have more reusable project configurations.
```
pytest --cobra MetaCoin.sol --import_remappings ["zeppeling=/my-zeppelin-checkout-folder"]
```

##### Allow paths
```
pytest --cobra MetaCoin.sol --allow_paths "/home/meheret,/user,/"
```

### Running test from compiled Contracts Json file (.json)

Compile your contracts into a package (soon to be ethPM-compliant)
```
solc --combined-json abi,bin,bin-runtime contracts/ > MetaCoin.json
```
Testing Contracts.json
```
pytest --cobra MetaCoin.json
```

### Running test from Yaml file (.yaml) 
`Comming Soon` with Cobra Framework

## Further help
##### PyTest
Go check out the [PyTest](http://pytest.org).

## Author ✒️

* **Meheret Tesfaye** - *Initial work* - [Cobra](https://github.com/cobraframework)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

