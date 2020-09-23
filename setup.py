#!/usr/bin/env python3

from setuptools import setup, find_packages

# read the contents of your README file
from os import path

with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()


setup(
    name="shcmd",
    version="0.7.3",
    description="Invoke command in shell.",
    long_description=long_description,
    author="so07",
    author_email="orlandini.se@gmail.com",
    url="https://github.com/so07/shcmd",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "shcmd=shcmd.main:main",
        ],
    },
)
