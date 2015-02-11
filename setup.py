#!/usr/bin/env python
from setuptools import setup, find_packages

import cmd

setup(

   name=cmd.name,
   version=cmd.version,
   description=cmd.description,
   author='so07',
   author_email='orlandini.se@gmail.com',
   url='https://github.com/so07/cmd',
   packages=find_packages(),

)
