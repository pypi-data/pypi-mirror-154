"""
waylonwalker uses setup tools for packaging.

To Build waylonwalker as a Python package

    $ python setup.py sdist bdist_wheel --bdist-dir ~/temp/bdistwheel

Regular install

    $ pip install -e .

To setup local Development

    $ pip install -e ".[dev]"

"""
from pathlib import Path

from setuptools import find_packages, setup

NAME = "waylonwalker"

README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")


setup(
    name=NAME,
    version="",
    description="Waylon Walker's business card",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
    url="https://github.com/waylonwalker/waylonwalker-cli",
    packages=find_packages(),
    platforms="any",
    license="OSI APPROVED :: MIT LICENSE",
    author="Waylon Walker",
    keywords="None",
    install_requires=["textual"],
    extras_require={"dev": ["flake8", "black", "setuptools", "wheel"]},
    entry_points={
        "console_scripts": ["waylonwalker = waylonwalker.__main__:main"],
    },
)
