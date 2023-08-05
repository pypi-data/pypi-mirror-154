from pathlib import Path
import setuptools

setuptools.setup(
    name="kelemipdf",
    version=1.1,
    long_description=Path("readme.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
