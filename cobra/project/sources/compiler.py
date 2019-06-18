from cobra.project.sources import *
from cobra.utils import file_reader, strip
from cobra.utils.console_log import console_log


def bytecode_link_to_md5(bytecode, contract_interface):
    count = 0
    contract_bytecode = []
    split_bytecode = re.split('__+', bytecode)
    files = bytecode_link_from_file(contract_interface)
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


def bytecode_link_from_file(contract_interface):
    files = []
    children = contract_interface['ast']['children']
    for attributes in children:
        try:
            file = attributes['attributes']['file']
            files.append(basename(file)[:-4])
        except KeyError:
            continue
    return files


def is_compiled(file_path, contract_interface):
    try:
        with open(file_path, 'r') as read_file:
            return_file = read_file.read()
            try:
                contract_interface_file = loads(return_file)['bin']
            except json.decoder.JSONDecodeError:
                return False
            contract_interface_compiled = loads(contract_interface)['bin']
            if contract_interface_compiled == contract_interface_file:
                read_file.close()
                return True
            read_file.close()
    except KeyError:
        return False
    except FileNotFoundError:
        return False
    return False


def to_compile(file_path_sol, allow_paths=None, import_remappings=None, more=False):
    if allow_paths is None:
        allow_paths = str(os.getcwd())

    if import_remappings is None:
        import_remappings = []

    solidity_contract = file_reader(file_path_sol)
    try:
        _import_remappings = ["-"]
        _import_remappings.extend(import_remappings)
        compiled_sol = compile_source(solidity_contract,
                                      allow_paths=allow_paths,
                                      import_remappings=_import_remappings)
    except solc.exceptions.SolcError as solcError:
        if more:
            console_log(str(solcError), "error", "Compile")
        else:
            console_log(str(solcError).split('\n')[0], "error", "Compile")
        sys.exit()
    contract_interface = compiled_sol['<stdin>:' + basename(file_path_sol)[:-4]]
    contract_interface['bin'] = bytecode_link_to_md5(contract_interface['bin'], contract_interface)
    contract_interface['bin-runtime'] = bytecode_link_to_md5(
        contract_interface['bin-runtime'], contract_interface)
    contract_name = """{\n "contractName": "%s",}""" % basename(file_path_sol)[:-4]
    artifact = web3.Web3().toText(dumps(contract_interface, indent=1).encode())
    artifact_contract_interface = "{%s}" % (strip(contract_name) +
                                            strip(artifact)[:-1] +
                                            strip(network))
    return artifact_contract_interface
