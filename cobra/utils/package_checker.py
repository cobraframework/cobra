from cobra.utils import *


# Package Checker
def package_checker(package_name: str, error_message: str, title: str):
    package = False
    installed_packages = pkg_resources.working_set
    package_keys = sorted(['%s' % installed_package.key
                           for installed_package in installed_packages])
    for package_key in package_keys:
        if package_key == package_name:
            package = True

    if not package:
        if error_message:
            console_log(error_message, "error", title)
        sys.exit()
