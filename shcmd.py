#!/usr/bin/env python
import sys
import os
import subprocess
import StringIO

from contextlib import closing

__all__ = ['execute', 'shcmd']


def _poll(p, stdout, stderr):

   stdout_iterator = iter(p.stdout.readline, b"")

   if stdout:
      stdout_context = open(stdout, 'w')
   else:
      stdout_context = closing(StringIO.StringIO())

   with stdout_context as fo:

      for o in stdout_iterator:
           print o,
           fo.write(o)
           fo.flush()


def execute (command, stdout=None, stderr=None, stdin=None, append=False):

   p = subprocess.Popen(command,
                        stdin  = subprocess.PIPE,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.STDOUT,
                        shell=True)

   _poll(p, stdout, stderr)

   _out, _err = p.communicate()

   return _out, _err


class shcmd:

   def __init__(self, command,
                      stdout = None, stderr = None, stdin = None,
                      msg = None,
                      append = False,
                      verbose = False,
                      debug = False):

      self._cmd = [command]

      self._stdout = stdout
      self._stderr = stderr
      self._stdin  = stdin

      self._msg    = msg

      self._append = append

      self._verbose = verbose
      self._debug  = debug


      self._out = None
      self._err = None


   def __str__(self):
      return str( " ".join(self._cmd) )

   def __call__(self):
      return self.execute()

   def __add__ (self, option):
      self._cmd.append(option)
      return self
   def __sub__ (self, option):
      self._cmd.insert(0, option)
      return self


   def execute (self):

      if self._msg:
          print "[SHCMD]", self._msg

      cmd_string = " ".join( self._cmd )

      print cmd_string
      if self._debug:
         return

      self._out, self._err = execute(cmd_string, self._stdout, self._stderr, self._stdin, self._append)

      return self._out


   def output(self):
      return self._out
   def error(self):
      return self._err

   def stdout(self):
      return self._stdout
   def stderr(self):
      return self._stderr
   def stdin(self):
      return self._stdin

