#!/usr/bin/env python3

from setuptools import setup, find_packages

from . import config

setup(
    name=config.name,
    version=config.version,
    description=config.description,
    author=config.author,
    author_email=config.author_email,
    url=config.url,
    packages=find_packages(),
    data_files=["shcmd.py"],
)
