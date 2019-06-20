from cobra import *


def network(more=False):
    configuration = Configuration()
    read_yaml = file_reader("./cobra.yaml")
    load_yaml = yaml_loader(read_yaml, more=more)
    if 'network' in load_yaml:
        network_yaml = load_yaml['network']
        configuration_yaml = configuration.network(network_yaml)
        return configuration_yaml
    else:
        console_log("network in cobra.yaml", "error", "NotFound")
        sys.exit()
