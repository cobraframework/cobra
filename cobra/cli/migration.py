from cobra.cli.network import _network
from cobra import *


def _migrate(more=False):
    network = _network(more)
    deployment = Deployment(network, more)
    configuration = Configuration()
    read_yaml = file_reader("./cobra.yaml")
    load_yaml = yaml_loader(read_yaml, more=more)
    if 'deploy' in load_yaml:
        deploy_yaml = load_yaml['deploy']
        configurations_yaml = configuration.deploy(deploy_yaml)
        # deployment.display_account()
        for configuration_yaml in configurations_yaml:
            if configuration_yaml['links'] is None:
                artifact_path_json = join(configuration_yaml['artifact_path'], configuration_yaml['artifact'])
                artifact_json = deployment.deploy_with_out_link(
                    configuration_yaml['artifact_path'],
                    configuration_yaml['artifact'], more=more)
                if artifact_json:
                    file_writer(artifact_path_json, str(artifact_json))
                continue
            else:
                artifact_path_json = join(configuration_yaml['artifact_path'], configuration_yaml['artifact'])
                artifact_json = deployment.deploy_with_link(
                    configuration_yaml['artifact_path'],
                    configuration_yaml['artifact'],
                    configuration_yaml['links'], more=more)
                if artifact_json:
                    file_writer(artifact_path_json, str(artifact_json))
                continue
    else:
        console_log("deploy in cobra.yaml", "error", "NotFound")
        sys.exit()
