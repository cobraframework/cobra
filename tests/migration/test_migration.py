from cobra.project.migration.deployment import Deployment
from cobra.project.configuration import Configuration
from cobra.utils import (
    file_reader,
    json_loader,
    yaml_loader
)

from os.path import join
import web3
import os


# Testing deployment
def test_migration():
    cobra_yaml = yaml_loader(file_reader("../cobra.yaml"), False)
    deployment = Deployment(
        Configuration().network(cobra_yaml['network']), False)
    configurations_deploy = Configuration().deploy(cobra_yaml['deploy'])

    for configuration_deploy in configurations_deploy:
        if configuration_deploy['links'] is None:
            assert os.path.isdir(configuration_deploy['artifact_path'])
            artifact_path_json = join(configuration_deploy['artifact_path'], configuration_deploy['artifact'])
            assert os.path.isfile(artifact_path_json)

            artifact_json = deployment.deploy_with_out_link(
                configuration_deploy['artifact_path'],
                configuration_deploy['artifact'], False)
            if artifact_json is not None:
                artifact_json = json_loader(artifact_json)
                for __network in artifact_json['networks'].keys():
                    deployed = artifact_json['networks'].get(__network)
                    assert isinstance(deployed['transactionHash'], str)
                    assert isinstance(deployed['contractAddress'], str)
                    # assert web3.isAddress(deployed['contractAddress'])
            else:
                raise AssertionError(None)
            continue
        else:
            # assert os.path.isdir(configuration_deploy['artifact_path'])
            # artifact_path_json = join(configuration_deploy['artifact_path'], configuration_deploy['artifact'])
            # assert os.path.isfile(artifact_path_json)
            #
            # artifact_json = deployment.deploy_with_link(
            #     configuration_deploy['artifact_path'],
            #     configuration_deploy['artifact'],
            #     configuration_deploy['links'], False)
            # if artifact_json is not None:
            #     artifact_json = json_loader(artifact_json)
            #     for __network in artifact_json['networks'].keys():
            #         deployed = artifact_json['networks'].get(__network)
            #         assert isinstance(deployed['transactionHash'], str)
            #         assert isinstance(deployed['contractAddress'], str)
            #         # assert web3.isAddress(deployed['contractAddress'])
            #
            #         assert deployed['links'][configuration_deploy['links'][0][:5]] == 'ConvertLib'
            #
            # else:
            #     raise AssertionError(None)
            continue
