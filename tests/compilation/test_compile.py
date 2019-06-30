from cobra.project.sources.compiler import to_compile
from cobra.utils import json_loader
from cobra import getcwd
from glob import glob

convertlib_bin = "60d061002f600b82828239805160001a6073146000811461001f57610021565bfe5" \
                 "b5030600052607381538281f3007300000000000000000000000000000000000000" \
                 "0030146080604052600436106056576000357c01000000000000000000000000000" \
                 "00000000000000000000000000000900463ffffffff16806396e4ee3d14605b575b" \
                 "600080fd5b608160048036038101908080359060200190929190803590602001909" \
                 "291905050506097565b6040518082815260200191505060405180910390f35b6000" \
                 "8183029050929150505600a165627a7a72305820ed6b1a354a80f6abd7a8fec8f89" \
                 "85957ce16123dfbd5aa58be7478935fc8626e0029"

metacoin_bin = "608060405234801561001057600080fd5b506127106000803273fffffffffffffffff" \
               "fffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16" \
               "8152602001908152602001600020819055506103fc806100656000396000f30060806" \
               "0405260043610610057576000357c0100000000000000000000000000000000000000" \
               "000000000000000000900463ffffffff1680637bd703e81461005c57806390b98a111" \
               "46100b3578063f8b2cb4f14610118575b600080fd5b34801561006857600080fd5b50" \
               "61009d600480360381019080803573fffffffffffffffffffffffffffffffffffffff" \
               "f16906020019092919050505061016f565b6040518082815260200191505060405180" \
               "910390f35b3480156100bf57600080fd5b506100fe600480360381019080803573fff" \
               "fffffffffffffffffffffffffffffffffffff16906020019092919080359060200190" \
               "92919050505061022f565b60405180821515151581526020019150506040518091039" \
               "0f35b34801561012457600080fd5b50610159600480360381019080803573ffffffff" \
               "ffffffffffffffffffffffffffffffff169060200190929190505050610388565b604" \
               "0518082815260200191505060405180910390f35b600073__ConvertLib__________" \
               "__________________6396e4ee3d61019484610388565b60026040518363ffffffff1" \
               "67c010000000000000000000000000000000000000000000000000000000002815260" \
               "0401808381526020018281526020019250505060206040518083038186803b1580156" \
               "101ed57600080fd5b505af4158015610201573d6000803e3d6000fd5b505050506040" \
               "513d602081101561021757600080fd5b8101908080519060200190929190505050905" \
               "0919050565b6000816000803373ffffffffffffffffffffffffffffffffffffffff16" \
               "73ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600" \
               "0205410156102805760009050610382565b816000803373ffffffffffffffffffffff" \
               "ffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526" \
               "0200190815260200160002060008282540392505081905550816000808573ffffffff" \
               "ffffffffffffffffffffffffffffffff1673fffffffffffffffffffffffffffffffff" \
               "fffffff168152602001908152602001600020600082825401925050819055508273ff" \
               "ffffffffffffffffffffffffffffffffffffff163373fffffffffffffffffffffffff" \
               "fffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628" \
               "f55a4df523b3ef846040518082815260200191505060405180910390a3600190505b9" \
               "2915050565b60008060008373ffffffffffffffffffffffffffffffffffffffff1673" \
               "ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002" \
               "05490509190505600a165627a7a72305820105c65272f03410067b9eeaa3d7df1125f" \
               "72a733c6940ec0656a949968ea81630029"


# Testing to_compile function
def test_to_compile():
    # Source MetaCoin and ConvertLib
    convertlib_path = "tests/sources/ConvertLib.sol"
    metacoin_path = "tests/sources/MetaCoin.sol"

    # Import remappings of MetaCoin
    print(str(getcwd()))
    print(glob(str(getcwd()) + '/tests/sources/*.*'))
    metacoin_import_remappings = ['=%s/tests/sources/' % str(getcwd())]

    # Compiling ConvertLib
    convertlib_compiled = to_compile(
        file_path_sol=convertlib_path,
        allow_paths=None,
        import_remappings=None
    )
    # Compiling MetaCoin
    metacoin_compiled = to_compile(
        file_path_sol=metacoin_path,
        allow_paths=None,
        import_remappings=metacoin_import_remappings
    )

    assert str(convertlib_bin) == json_loader(convertlib_compiled)['bin']

    assert str(metacoin_bin) == json_loader(metacoin_compiled)['bin']
