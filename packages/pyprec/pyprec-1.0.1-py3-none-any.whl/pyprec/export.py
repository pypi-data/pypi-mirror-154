"""This module"""
import logging
from pathlib import Path
import subprocess as sp
from .pyexporter import load_fill_and_export
from .utils.utils import boldface, get_template_path
from pyprec import PACKAGE

logger = logging.getLogger(PACKAGE)


def create_folder_tree(prefix_folder: Path, source_folder: Path):
    """Creates the source directory tree.

    Directory tree is:

    .. code-block:: text

        root
        |-- source_folder # ``src/<pkgname>``
        |       |-- scripts
        |       |-- utils


    Parameters
    ----------
    prefix_folder: Path
        The package root folder.
    source_folder: Path
        The folder to create the package source files to.

    Raises
    -------
    FileExistsError
        If the source directory already exists.
    """
    prefix_folder.joinpath(".github/workflows").mkdir(parents=True)
    source_folder.parent.mkdir(parents=True)
    source_folder.mkdir()
    source_folder.joinpath("scripts").mkdir()
    source_folder.joinpath("utils").mkdir()


def create_package_light(setup: dict):
    """Light wrapper function to copy template in package destination folder.

    Parameters
    ----------
    setup: dict
        The key-value pairs to be inserted in the template fields.
    """
    prefix_folder = setup["prefix_folder"]
    source_folder = prefix_folder / f"src/{setup['pkgname']}"
    create_folder_tree(prefix_folder, source_folder)

    # __init__ files
    source_folder.joinpath("scripts/__init__.py").touch()
    source_folder.joinpath("utils/__init__.py").touch()
    load_fill_and_export("initfile.inc", setup, source_folder / "__init__.py")

    # setup files
    load_fill_and_export("pyproject.inc", setup, prefix_folder / "pyproject.toml")
    load_fill_and_export("setup.inc", setup, prefix_folder / "setup.cfg")

    # configlog file
    utils_folder = source_folder / "utils"
    load_fill_and_export("configlog.inc", setup, utils_folder / "configlog.py")

    # entry point file
    script_folder = source_folder / "scripts"
    load_fill_and_export(
        "main_script.inc", setup, script_folder / f"{setup['pkgname']}.py"
    )

    # workflows files
    workflow_folder = prefix_folder / ".github/workflows"
    load_fill_and_export(
        "pytest.inc", setup, workflow_folder / f"pytest.yaml"
    )
    load_fill_and_export(
        "pythonpublish.inc", setup, workflow_folder / f"pythonpublish.yaml"
    )

    # CITATION.cff placeholder
    load_fill_and_export(
        "CITATION.inc", setup, prefix_folder / f"CITATION.cff"
    )

    # sphinx docs
    if setup["should_run_sphinx"]:
        docs_folder = prefix_folder / "docs"
        docs_folder.mkdir()
        project_name = setup["pkgname"]
        author = setup["author"]
        version = setup["version"]
        template_folder = get_template_path("sphinx")
        cmd = (
            f"sphinx-quickstart --sep -p {project_name} -a '{author}' -r {version} "
            "-l en --makefile --ext-autodoc --ext-viewcode "
            f"--extensions sphinxcontrib.napoleon -t {template_folder} {docs_folder}"
        )
        try:
            cmd_output = sp.run(cmd, shell=True, capture_output=True, check=True)
        except sp.CalledProcessError as err:
            logger.error("".join(["\n[ERROR](pyprec) ", err.stderr.decode("utf-8")]))
            raise
        logger.debug("Quickstarting sphinx documentation ... \n")
        logger.debug(cmd_output.stdout.decode("utf-8"))
        logger.debug("Run command `make apidoc` in the docs directory to produce automatic function documentation.")
        
        # read the docs yaml
        load_fill_and_export(
            "readthedocs.inc", setup, prefix_folder / f".readthedocs.yml"
        )

    msg = boldface(
        f"{setup['pkgname']} package successfully created at {prefix_folder}"
    )
    logger.info(msg)
