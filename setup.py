"""
Python setup script.
:author: Samuel Terra <samuelterra22@hotmail.com>
:license: MIT, see license file or https://opensource.org/licenses/MIT
:created on 2020-01-25
:last modified by: Samuel Terra
:last modified time: 2020-01-25
"""

from setuptools import setup
import io
import os


def read(*names, **kwargs):
    try:
        with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8"),
        ) as fp:
            return fp.read()
    except IOError:
        return ""


long_description = read("README.md")

setup(
    version="1.0",
    name="Analysis-of-antenna-coverage",
    author="Samuel Terra",
    author_email="samuelterra22@gmail.com",
    packages=[""],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samuelterra22/Analysis-of-antenna-coverage",
    license="GNU General Public License v3.0",
    description="A software for simulating the radio frequency spectrum transmitting voice to base stations.",
)
