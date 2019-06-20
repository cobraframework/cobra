from cobra import *


def pytest(more=False):
    _pytest = False
    _pytest_cobra = False
    installed_packages = pkg_resources.working_set
    package_keys = sorted(['%s' % installed_package.key
                           for installed_package in installed_packages])
    for package_key in package_keys:
        if package_key == 'pytest':
            _pytest = True
        elif package_key == 'pytest-cobra':
            _pytest_cobra = True
        else:
            pass

    if not _pytest:
        console_log("Install pytest framework 'pip install pytest'!",
                    "error", "NotFound")
        sys.exit()
    elif not _pytest_cobra:
        console_log("Install pytest-cobra 'pip install pytest-cobra'!",
                    "error", "NotFound")
        sys.exit()
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
