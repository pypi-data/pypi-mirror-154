"""This module implements the ``pyprec`` user interface."""
import logging
from typing import Any, Tuple
from pathlib import Path
from .utils.utils import load_runcard, boldface
from .utils.ask_question import ask_question
from pyprec import __version__, PACKAGE

logger = logging.getLogger(PACKAGE)


def ask_question_list(
    logger: logging.Logger, questions: list[Tuple[str, str, Any]], timeout: float
) -> dict:
    """Asks interactively to edit the runcard.

    Receives the input from the user and opens an editor in the terminal as a
    subprocess. Default editor is nano, otherwise the `QUAKE_EDITOR` environment
    variable allows for custom choice.

    Parameters
    ----------
    logger: logging.Logger
        The logger instance.
    questions: list[Tuple[str, str, Any]
        List of tuples containing (key, question, default answer).
    timeout: float
        Time limit to answer in seconds.

    Returns
    -------
    setup: dict
        The key-value pairs to be inserted in the template fields.
    """
    # immediately check that the prefix folder does not contain any src/pkgname
    setup = {}
    while True:
        k_folder, q_folder, d_folder = questions[0]
        prefix_folder = ask_question(logger, q_folder, d_folder, timeout=timeout)
        if not Path(prefix_folder).joinpath("src").is_dir():
            setup[k_folder] = prefix_folder
            break
        logger.info(
            "The prefix folder already contains a src directory, please set another path..."
        )
    setup.update(
        {
            key: ask_question(logger, question, default, timeout=timeout)
            for key, question, default in questions[1:]
        }
    )
    return setup


def get_question_list() -> list[Tuple[str, str, Any]]:
    """Returns the list of questions to be asked to the user with default values.

    Returns
    -------
    questions: list[Tuple[str, str, Any]]
        List of tuples containing (key, question, default answer).
    """
    questions = [
        ("prefix_folder", "> Prefix folder [.]: ", "."),
        ("pkgname", "> Package name: ", None),
        ("version", "> Package version [1.0.0]: ", "1.0.0"),
        ("author", "> Author: ", None),
        ("author_email", "> Author email: ", None),
        ("description", "> Project description: ", None),
        ("python_requires", "> Minimum Python version required: ", None),
        (
            "dependencies",
            "> Project dependencies (comma separated list) [no-deps]: ",
            "no-deps",
        ),
        (
            "make_sphinx_docs",
            "> Do you want to run sphinx to make package documentation? [y/n] ",
            None,
        ),
    ]
    return questions


def refine_setup_dict(setup):
    """Refine some dictionary keys to work with code.

    Parameters
    ----------
    setup: dict
        The key-value pairs to be inserted in the template fields.
    """
    setup["prefix_folder"] = Path(setup["prefix_folder"])
    deps = setup["dependencies"]
    if deps and deps != "no-deps":
        deps_list = [dep.strip() for dep in deps.split(",") if "tensorflow" not in dep]
        setup["dependencies"] = "".join(["\n    ", "\n    ".join(deps_list)])
        # check if tensorflow is in dependencies
        tfs = ["tensorflow", "tensorflow-cpu", "tensorflow-gpu", "tensorflow-rocm"]
        setup["use_tf"] = "" if any(tf in deps for tf in tfs) else "# "
    else:
        setup["dependencies"] = ""
        setup["use_tf"] = "# "

    setup["should_run_sphinx"] = setup["make_sphinx_docs"].lower() == "y"
    setup["use_sphinx"] = "" if setup["should_run_sphinx"] else "# "


def ui() -> dict:
    """PyPReC user interface implementation.

    Returns
    -------
    setup: dict
        The key-value pairs to be inserted in the template fields.
    """
    timeout = 600
    msg = boldface(f"Welcome to the PyPReC {__version__} user interface.\n")
    msg += """Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).
        """
    logger.info(msg)

    questions = get_question_list()
    setup = ask_question_list(logger, questions, timeout)

    refine_setup_dict(setup)

    return setup


def load_setup_from_runcard(runcard_file: Path) -> dict:
    """Load runcard from yaml file.

    Parameters
    ----------
    runcard_file: Path
        The yaml to load the dictionary from.

    Returns
    -------
    runcard: dict
        The loaded settings dictionary.
    """
    setup = load_runcard(runcard_file)
    refine_setup_dict(setup)
    return setup
