"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # This is the name of your project
    # Can be installed using- $ pip install sampleproject
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    name="MachineLearningModule",  # Required
    version="0.0.1",
    description="This module is developed to replicate the functionalities of sklearn to run and implement ML models.",
    url="https://github.com/pypa/sampleproject",  # Optional
    # This should be your name or the name of the organization which owns the
    # project.
    author="Pratik Khandelwal",  # Optional
    # This should be a valid email address corresponding to the author listed
    # above.
    author_email="pratikkhandelwal68@gmail.com",
    long_description="This module is developed to replicate the functionalities of sklearn to run and implement ML models.",
    packages=find_packages(),  # Required
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.7, <4",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/discussions/install-requires-vs-requirements/
    install_requires=[
        "pandas",
    ],  # Optional
)