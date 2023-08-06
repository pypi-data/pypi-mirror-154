"""This module implements general utility functions."""
from importlib.resources import files
from pathlib import Path, PosixPath
from string import Template, ascii_uppercase
import yaml


def get_template_path(template_name: str) -> Path:
    """Returns the query template as a Path.

    This implementation retrieves the query path independently of the directory
    where the Python interpreter has been run from.

    Parameters
    ----------
    template_name: str
        The name of the template to be found in the source file.

    Returns
    -------
    Path
        The path to the query template.
    """
    return files("pyprec.templates").joinpath(template_name)


# ------------------------------------------------------------------------------
# runcard utilities


def path_constructor(loader, node):
    """PyYaml utility function."""
    value = loader.construct_scalar(node)
    return Path(value)


def path_representer(dumper, data):
    """PyYaml utility function."""
    return dumper.represent_scalar("!Path", "%s" % data)


def load_runcard(runcard_file: Path) -> dict:
    """Load runcard from yaml file.

    Parameters
    ----------
    runcard_file: Path
        The yaml to load the dictionary from.

    Returns
    -------
    runcard: dict
        The loaded settings dictionary.

    Note
    ----
    The pathlib.Path objects are automatically loaded if they are encoded
    with the following syntax:

    .. code-block:: yaml

        path: !Path 'path/to/file'
    """
    if not isinstance(runcard_file, Path):
        runcard_file = Path(runcard_file)

    yaml.add_constructor("!Path", path_constructor)
    with open(runcard_file, "r") as stream:
        runcard = yaml.load(stream, Loader=yaml.FullLoader)
    return runcard


def save_runcard(fname: Path, setup: dict):
    """Save runcard to yaml file.

    Parameters
    ----------
    fname: Path
        The yaml output file.
    setup: Path
        The settings dictionary to be dumped.

    Note
    ----
    pathlib.PosixPath objects are automatically loaded.
    """
    yaml.add_representer(PosixPath, path_representer)
    with open(fname, "w") as f:
        yaml.dump(setup, f, indent=4)


# ------------------------------------------------------------------------------
# Template utilities


def get_mapping_from_args(arg: dict = {}, /, **kwargs) -> dict:
    """Unifies the parameters in a unique dictionary map.

    If there are duplicates between ``arg`` dictionary keys and any parameter in
    ``**kwargs``, keyword arguments have always the returned dictionary.

    Parameters
    ----------
    arg: dict
        The input dictionary.
    **kwargs
        Optional keyword arguments.

    Returns
    -------
    mapping: dict
        The unique output mapping.
    """
    return arg | kwargs


class CaseSensitiveTemplate(Template):
    """Class re-defining Template for case sensitive string substitution.

    The ``substitute`` and ``safe_substitute`` methods treat differently the
    placeholders with different capitalization in the template file.

    Example
    --------
    >>> template = '''
    ... ${prefix} is lower-case
    ... ${Prefix} is capitalized
    ... ${PREFIX} is uppercase
    ... '''
    >>> t = CaseSensitiveTemplate(template)
    >>> replace_dict = {"prefix": "foo"}
    >>> subs = t.substitute(replace_dict)
    >>> print(subs)
    foo is lower-case
    Foo is capitalized
    FOO is uppercase
    """

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)

    def do_template_based_capitalization(self, mapping: dict):
        """Adds capitalized or full uppercase keys to replace dictionary.

        Parameters
        ----------
        mapping: dict
            The key-value pairs to be inserted in the template fields.
        """
        matches = self.pattern.findall(self.template)
        for match in matches:
            key = next(filter(None, match))
            if key and key[0] in ascii_uppercase:
                if key == key.upper():
                    # full uppercase
                    mapping[key.upper()] = mapping[key.lower()].upper()
                else:
                    # first letter capitalization
                    mapping[key.capitalize()] = mapping[key.lower()].capitalize()

    def safe_substitute(self, mapping={}, /, **kwds) -> str:
        """Safe substitution methods with case sensitive capitalization.

        Refer to `docs <https://docs.python.org/3/library/string.html#string.Template>`_
        for function documentation.
        """
        new_mapping = get_mapping_from_args(mapping, **kwds)
        self.do_template_based_capitalization(new_mapping)
        return super().safe_substitute(new_mapping)

    def substitute(self, mapping={}, /, **kwds) -> str:
        """Safe substitution methods with case sensitive capitalization.

        Refer to `docs <https://docs.python.org/3/library/string.html#string.Template>`_
        for function documentation.
        """
        new_mapping = get_mapping_from_args(mapping, **kwds)
        self.do_template_based_capitalization(new_mapping)
        return super().substitute(new_mapping)


# ------------------------------------------------------------------------------
# console utilities


def get_color_to_sgr_codes() -> dict:
    """Return Select Graphic Rendiction (SGR) sequence in dictionary form.

    Note
    ----
    Check out this `link <https://chrisyeh96.github.io/2020/03/28/terminal-colors.html>`_
    for more information about terminal colors and SGR codes.

    Returns
    -------
    codes: dict
        The terminal colorcodes
    """
    codes = {"default": "\x1b[0m"}

    _colors = [
        ("black", "gray"),
        ("red", "light red"),
        ("green", "light green"),
        ("yellow", "light yellow"),
        ("blue", "light blue"),
        ("magenta", "light magenta"),
        ("cyan", "light cyan"),
        ("white", "bright white"),
    ]

    for i, (dark, light) in enumerate(_colors, 30):
        codes[dark] = "\x1b[%im" % i
        codes[light] = "\x1b[%im" % (i + 60)
    return codes


def colorize(text: str, color: str) -> str:
    """Changes the printed color of the input string.

    If the color name does not exists, returns default color.

    Parameters
    ----------
    text: str
        The text to be colored.
    color: str
        The color name.
    """
    codes = get_color_to_sgr_codes()
    code = codes.get(color, None)
    if code is None:
        return text
    return "".join([codes[color], text, codes["default"]])


def boldface(text: str) -> str:
    """Returns input boldface version.

    Parameters
    ----------
    text: str
        The test to be boldfaced.

    Return
    ------
    str
        The boldface version of the input.
    """
    return "".join(["\x1b[1m", text, "\x1b[0m"])
