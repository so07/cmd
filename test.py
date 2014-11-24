#!/usr/bin/env python

from cmd import cmd

a = cmd('echo')

a += 'Hello World!'

a()

print a.output()
