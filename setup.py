"""
    Setup file for yglu.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.0.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup
import site
import sys

# needed for "pip install -e .", see https://github.com/pypa/pip/issues/7953
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

if __name__ == "__main__":
    try:
        setup(use_scm_version=True)
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
