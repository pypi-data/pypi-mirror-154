import setuptools
from pathlib import Path

setuptools.setup(
    name = "mvinittipdf", 
    version = 1.1,
    author = "Masheed",
    long_description = Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)