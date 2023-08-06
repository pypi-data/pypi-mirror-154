import logging
from pathlib import Path
from .utils.utils import get_template_path, CaseSensitiveTemplate
from pyprec import PACKAGE

logger = logging.getLogger(PACKAGE)


def load_fill_and_export(template_path: Path, setup: dict, output_path: Path):
    """Wrapper function that loads a template file, fills and writes it to file.

    Parameters
    ----------
    template_path: Path
        The input template file path.
    setup: dict
        The key-value pairs to be inserted in the template fields.
    output_path: Path
        The output file path.
    """
    loaded_file = PyExporter(get_template_path(template_path))
    loaded_file.substitute(setup)
    loaded_file.write(output_path)


class PyExporter:
    """Class providing templating utilities.

    Example
    -------

    Loading a template from a ``.inc`` file:

    >>> from pyprec.pyexporter import PyExporter
    >>> exporter = PyExporter("foo.inc")
    >>> exporter.fill(replace_dict)
    >>> exporter.write("foo.py")
    """

    def __init__(self, input_path: Path):
        """
        Parameters
        ----------
        input_path: Path
            The path to the input ``.inc`` file.
        """
        self.infile_path = input_path
        self.template = CaseSensitiveTemplate(input_path.read_text())
        self.filled_string = None
        self.__is_filled = False

    def substitute(self, setup: dict):
        """Fills the input template with dictionary key-value pair substitution.

        Parameters
        ----------
        setup: dict
            The key-value pairs to be inserted in the template fields.

        Raises
        ------
        KeyError
            If not all the fields in the template file are filled.
        """
        self.filled_string = self.template.substitute(setup)
        self.__is_filled = True

    def write(self, output_path: Path):
        """Dumps template to file.

        Parameters
        ----------
        output_path: Path
            The output file path.
        """
        if not self.__is_filled:
            logger.warning(
                f"Trying to export incomplete template to {output_path}, code might be broken"
            )
        output_path.write_text(self.filled_string)
        logger.debug(f"Exported file to {output_path}")
