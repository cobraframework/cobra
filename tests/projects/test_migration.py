#!/usr/bin/python3
import os

from cobra.utils import Style, Fore


def deploy_success_output(contract_name: str):
    return Style.DIM + Fore.GREEN + "[SUCCESS]" + Style.RESET_ALL + " " + \
           Fore.WHITE + "Deploy" + ': ' + Style.RESET_ALL + "%s done!" % contract_name


def deploy_warning_output(contract_name: str):
    return Style.DIM + Fore.YELLOW + "[WARNING]" + Style.RESET_ALL + " " + \
           Fore.WHITE + "Deploy" + ': ' + Style.RESET_ALL + "Already deployed.%s" % contract_name


def test_cli_compile(cli_tester, project_path, capsys):
    cli_tester('compile')
    cli_tester.close()


def test_cli_deploy(cli_tester, project_path, capsys):
    cli_tester('deploy')
    output, error = capsys.readouterr()
    assert str(output).split('\n')[1] == deploy_success_output('ConvertLib')
    assert str(output).split('\n')[5] == deploy_success_output('MetaCoin')
    cli_tester.close()
    cli_tester('deploy --more')
    output, error = capsys.readouterr()
    assert str(output).split('\n')[0] == deploy_warning_output('ConvertLib')
    assert str(output).split('\n')[1] == deploy_warning_output('MetaCoin')
    cli_tester.close()
    os.remove('contracts/ConvertLib.json')
    os.remove('contracts/MetaCoin.json')

