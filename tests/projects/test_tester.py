#!/usr/bin/python3
import os


def test_run_compile(cli_tester, project_path, capsys):
    cli_tester('compile')
    cli_tester.close()


def test_cli_unittest(cli_tester, project_path, capsys):
    cli_tester('test')
    output, error = capsys.readouterr()
    assert output == str()
    cli_tester.close()
    cli_tester('test --unittest')
    cli_tester.close()
    os.remove('contracts/ConvertLib.json')
    os.remove('contracts/MetaCoin.json')
