"""Package source root directory. """
from importlib.metadata import metadata
from ${pkgname}.utils.configlog import PACKAGE

__version__ = metadata(PACKAGE)["version"]