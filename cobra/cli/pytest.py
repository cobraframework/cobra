from cobra import *
from cobra.utils import package_checker


def _pytest(more=False):
    package_checker("pytest",
                    "Install pytest framework 'pip install pytest'!",
                    "PyTestNotFound")
    package_checker("pytest-cobra",
                    "Install pytest-cobra 'pip install pytest-cobra'!",
                    "PyTestCobraNotFound")
    try:
        read_yaml = file_reader("./cobra.yaml")
        load_yaml = yaml_loader(read_yaml, more=more)
        test_yaml = load_yaml['test']
        try:
            _test = ['--cobra', 'cobra.yaml']
            test_paths = test_yaml['test_paths']
            for test_path in test_paths:
                tests = glob(join(Path(test_path).resolve(), "*_test.py"))
                for test in tests:
                    _test.append(test)
            __import__("pytest").main(_test)
        except KeyError:
            console_log("test_paths in test", "error", "NotFound")
            sys.exit()

    except KeyError:
        console_log("test in cobra.yaml", "error", "NotFound")
        sys.exit()
