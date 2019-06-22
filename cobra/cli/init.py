from cobra import *


"""
Download a template Greeter contract file and extract its contents in memory
yields (filename, file-like object) pairs
"""


def _init(url=None):
    if url is None:
        url = "https://raw.githubusercontent.com/meherett/cobra/master/cobra/cli/template/Greeter.zip?token=AHMADHKX5ZOC4OUFOYUMQUS5BVK3C"
    try:
        response = requests.get(url)
        with zipfile.ZipFile(io.BytesIO(response.content)) as _zips:
                _zips.extractall(getcwd())
    except requests.exceptions.MissingSchema as missingSchema:
        console_log(str(missingSchema), "error", "MissingSchema")
        sys.exit()
    except requests.exceptions.InvalidSchema as invalidSchema:
        console_log(str(invalidSchema), "error", "InvalidSchema")
        sys.exit()
    except zipfile.BadZipFile as badZipFile:
        console_log(str(badZipFile), "error", "BadZipFile")
        sys.exit()
