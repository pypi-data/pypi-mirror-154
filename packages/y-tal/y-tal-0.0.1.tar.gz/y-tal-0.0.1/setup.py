import setuptools
from tal import __version__ as tal_version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="y-tal",
    version=tal_version,
    author="Diego Royo & Pablo Luesia",
    author_email="droyo@unizar.es",
    description="Transient Auxiliary Library - Analysis and processing of time-resolved light transport",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diegoroyo/tal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
