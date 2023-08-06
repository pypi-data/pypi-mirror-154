"""Package source root directory. """
from importlib.metadata import metadata
from pyprec.utils.configlog import PACKAGE

__version__ = metadata(PACKAGE)["version"]
