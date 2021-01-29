import subprocess
from pathlib import Path

from datajob import logger


class DatajobPackageWheelError(Exception):
    """any exception occuring when constructing a wheel in data job context."""


def create(project_root: str, package: str) -> None:

    wheel_functions = {
        "pip": _setuppy_wheel,
        "pipenv": _setuppy_wheel,
        "poetry": _poetry_wheel,
    }
    wheel_functions[package](project_root)


def _setuppy_wheel(project_root):
    """launch a subprocess to built a wheel.
    todo - use the setuptools/disttools api to create a setup.py.
    relying on a subprocess feels dangerous.
    """
    setup_py_file = Path(project_root, "setup.py")
    if setup_py_file.is_file():
        logger.debug(f"found a setup.py file in {project_root}")
        cmd = f"cd {project_root}; python setup.py bdist_wheel"
        _call_create_wheel_command(cmd=cmd)
    else:
        raise DatajobPackageWheelError(
            f"no setup.py file detected in project root {project_root}. "
            f"Hence we cannot create a python wheel for this project"
        )


def _poetry_wheel(project_root):
    """launch a subprocess to built a wheel.
    todo - use the setuptools/disttools api to create a setup.py.
    relying on a subprocess feels dangerous.
    """
    poetry_file = Path(project_root, "pyproject.toml")
    if poetry_file.is_file():
        logger.debug(f"found a pyproject.toml file in {project_root}")
        cmd = f"cd {project_root}; poetry build"
        _call_create_wheel_command(cmd=cmd)
    else:
        raise DatajobPackageWheelError(
            f"no pyproject.toml file detected in project root {project_root}. "
            f"Hence we cannot create a python wheel for this project"
        )


def _call_create_wheel_command(cmd: str) -> None:
    logger.debug("creating wheel")
    print(f"wheel command: {cmd}")
    # todo - shell=True is not secure
    subprocess.call(cmd, shell=True)
