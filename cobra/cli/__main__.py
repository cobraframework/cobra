from cobra.cli import *
from cobra.utils.console_log import console_log


usage = "[-h] [help] [init] [compile {--more}] [deploy {--more}] [migrate {--more}] " \
        "[test {--unittest} or {--pytest}, {--more}]"

description = textwrap.dedent('''\
        Cobra Framework is a development environment, testing framework and asset
        pipeline for blockchains using the Ethereum Virtual Machine (EVM), 
        https://github.com/cobraframework''')


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="cobra",
        usage=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
                !!!PLEASE HELP US!!!
        Bitcoin: 1BZv4gKoX9UAyfxX6WEBRxnqnd4oTqncYo
        Ethereum: 0xA963a015d355F08d82cDDD815FFe758f0092fE57
        '''),
        description=description)

    parser.set_defaults(init=False, compile=False, deploy=False, migrate=False,
                        test=False, unittest=False, pytest=False, help=False)

    cobra_parser = parser.add_subparsers(
        title="COBRA FRAMEWORK",
        description=textwrap.dedent('''\
                    Cobra commands list below here!'''))

    parser_help = cobra_parser.add_parser('help')
    parser_help.add_argument('help', action='store_true',
                             help='Show this help message and exit')

    parser_help = cobra_parser.add_parser('init')
    parser_help.add_argument('init', action='store_true',
                             help='Clone template!')

    parser_compile = cobra_parser.add_parser('compile')
    parser_compile.add_argument("compile", action='store_true',
                                help='compile contract source files')
    parser_compile.add_argument('-m', '--more', action='store_true',
                                help='View more errors [compile]')

    parser_migrate = cobra_parser.add_parser('migrate')
    parser_migrate.add_argument(dest="migrate", action='store_true',
                                help='Alias for deploy')
    parser_migrate.add_argument('-m', '--more', action='store_true',
                                help='View more errors [migrate]')

    parser_deploy = cobra_parser.add_parser('deploy')
    parser_deploy.add_argument("deploy", action='store_true',
                               help='Run deploy to deploy compiled contracts')
    parser_deploy.add_argument('-m', '--more', action='store_true',
                               help='View more errors [deploy]')

    parser_test = cobra_parser.add_parser('test')
    parser_test.add_argument("test", action='store_true',
                             help="Run Python test by default [Unittest]. There are two types of testing framework "
                                  "Unittest and Pytest. Unittest https://docs.python.org/3/library/unittest.html "
                                  "and Pytest https://docs.pytest.org/en/latest/")
    parser_test.add_argument('-u', '--unittest', action='store_true',
                             help='Run Python builtin tests vie [Unittest]')
    parser_test.add_argument('-p', '--pytest', action='store_true',
                             help='Run Python tests vie [PyTest] but, First install pytest and plugin pytest-cobra '
                                  'using pip [pip install pytest-cobra] '
                                  'or https://github.com/cobraframework/pytest-cobra')
    parser_test.add_argument('-m', '--more', action='store_true',
                             help='View more errors [test]')
    # Cobra Agreements
    cobra_args = parser.parse_args()

    if not argv:
        console_log(usage, title="Usage")

    elif cobra_args.help:
        parser.print_help()

    elif cobra_args.init:
        _init(None)

    elif cobra_args.compile and not \
            cobra_args.more:
        _compile(False)
    elif cobra_args.compile and \
            cobra_args.more:
        _compile(True)

    elif cobra_args.migrate and not \
            cobra_args.more:
        _migrate(False)
    elif cobra_args.migrate and \
            cobra_args.more:
        _migrate(True)

    elif cobra_args.deploy and not \
            cobra_args.more:
        _migrate(False)
    elif cobra_args.deploy and \
            cobra_args.more:
        _migrate(True)

    elif cobra_args.test and not cobra_args.unittest\
            and not cobra_args.pytest and not cobra_args.more:
        _unittest(False)
    elif cobra_args.test and not cobra_args.unittest\
            and not cobra_args.pytest and cobra_args.more:
        _unittest(True)

    elif cobra_args.unittest and not \
            cobra_args.more:
        _unittest(False)
    elif cobra_args.unittest and \
            cobra_args.more:
        _unittest(True)

    elif cobra_args.pytest and not \
            cobra_args.more:
        _pytest(False)
    elif cobra_args.pytest and \
            cobra_args.more:
        _pytest(True)

    # parser.exit()
