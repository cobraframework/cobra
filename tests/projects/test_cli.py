from cobra.utils import *
import pytest


@pytest.mark.datafiles(os.path.join(os.getcwd(), '/tests/cobra.yaml'))
def test_cobra(script_runner):
    cobra = script_runner.run('cobra', '--help')
    assert cobra.success


# @pytest.mark.datafiles('/home/meheret/PycharmProjects/Cobra/tests/cobra.yaml')
def test_compile(script_runner):
    _compile = script_runner.run('cobra', 'compile')
    assert _compile.success
    # assert _compile.stdout == \
    #        Style.DIM + Fore.YELLOW + "[WARNING]" + Style.RESET_ALL + ' ' + \
    #        Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
    #        "ConvertLib.sol already compiled in tests/contracts/ConvertLib.json\n" + \
    #        Style.DIM + Fore.YELLOW + "[WARNING]" + Style.RESET_ALL + ' ' + \
    #        Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
    #        "MetaCoin.sol already compiled in tests/contracts/MetaCoin.json" + "\n"

    _compile_more = script_runner.run('cobra', 'compile', '--more')
    assert _compile_more.success
    # assert _compile_more.stdout == \
    #        Style.DIM + Fore.YELLOW + "[WARNING]" + Style.RESET_ALL + ' ' + \
    #        Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
    #        "ConvertLib.sol already compiled in tests/contracts/ConvertLib.json\n" + \
    #        Style.DIM + Fore.YELLOW + "[WARNING]" + Style.RESET_ALL + ' ' + \
    #        Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
    #        "MetaCoin.sol already compiled in tests/contracts/MetaCoin.json" + "\n"


def test_deploy(script_runner):
    _deploy = script_runner.run('cobra', 'deploy')
    assert _deploy.success
    # assert _deploy.stdout == \
    #        Style.DIM + Fore.GREEN + "[WARNING]" + Style.RESET_ALL + ' ' + \
    #        Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
    #        "ConvertLib.sol already compiled in tests/contracts/ConvertLib.json\n" + \
    #        Style.DIM + Fore.GREEN + "[WARNING]" + Style.RESET_ALL + ' ' + \
    #        Fore.WHITE + "Compile" + ': ' + Style.RESET_ALL + \
    #        "MetaCoin.sol already compiled in tests/contracts/MetaCoin.json" + "\n"
    _deploy_more = script_runner.run('cobra', 'deploy', '--more')
    assert _deploy_more.success
    # assert _deploy_more.stdout == ""


def test_unittest(script_runner):
    _unittest = script_runner.run('cobra', 'test')
    assert _unittest.success
    # assert _unittest.stdout == console("[ERROR]", "FileNotFoundError",
    #                                    "No such file or directory './cobra.yaml'\n")
    _unittest = script_runner.run('cobra', 'test', '--unittest')
    assert _unittest.success
    # assert _unittest.stdout == console("[ERROR]", "FileNotFoundError",
    #                                    "No such file or directory './cobra.yaml'\n")
    _unittest_more = script_runner.run('cobra', 'test', '--more')
    assert _unittest_more.success
    # assert _unittest_more.stdout == console("[ERROR]", "FileNotFoundError",
    #                                         "No such file or directory './cobra.yaml'\n")
    _unittest_more = script_runner.run('cobra', 'test', '--unittest', '--more')
    assert _unittest_more.success
    # assert _unittest_more.stdout == console("[ERROR]", "FileNotFoundError",
    #                                         "No such file or directory './cobra.yaml'\n")


def test_pytest(script_runner):
    _pytest = script_runner.run('cobra', 'test', '--pytest')
    assert _pytest.success
    # assert _pytest.stdout == console("[ERROR]", "FileNotFoundError",
    #                                  "No such file or directory './cobra.yaml'\n")
    _pytest_more = script_runner.run('cobra', 'test', '--pytest', '--more')
    assert _pytest_more.success
    # assert _pytest_more.stdout == console("[ERROR]", "FileNotFoundError",
    #                                       "No such file or directory './cobra.yaml'\n")
