#!/usr/bin/env python
import sys
import os
import subprocess
import StringIO

from contextlib import closing

__all__ = ['execute', 'shcmd']


def _poll(p, stdout, stderr, stdmode):

   stdout_iterator = iter(p.stdout.readline, b"")

   if stdout:
      stdout_context = open(stdout, stdmode)
   else:
      stdout_context = closing(StringIO.StringIO())

   stdout_save = ''

   with stdout_context as fo:

      for o in stdout_iterator:
           print o,
           fo.write(o)
           fo.flush()
           stdout_save += o

   return stdout_save.strip(), ''

def execute (command, stdout=None, stderr=None, stdin=None, stdmode='a'):

   p = subprocess.Popen(command,
                        stdin  = subprocess.PIPE,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.STDOUT,
                        shell=True)

   _out, _err = _poll(p, stdout, stderr, stdmode)

   _out2, _err2 = p.communicate()

   if _out2:
      _out += _out2

   if _err2:
      _err += _err2

   return _out, _err


class shcmd:

   def __init__(self, command,
                      stdout = None, stderr = None, stdin = None,
                      msg = None,
                      append = False,
                      silent = False,
                      verbose = False,
                      debug = False):

      self._cmd = [command]

      self._stdout = stdout
      self._stderr = stderr
      self._stdin  = stdin

      self._msg    = msg

      self._append = append
      self._silent = silent
      self._verbose = verbose
      self._debug  = debug

      self._out = None
      self._err = None

      self._stdmode = 'w'
      if self._append:
         self._stdmode = 'a'


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

      if self._msg and not self._silent:
          print "[SHCMD]", self._msg

      cmd_string = " ".join( self._cmd )

      if not self._silent:
         print "[SHCMD]", cmd_string

      if self._debug:
         return

      if self._stdout:
         if self._verbose:
            print "[SHCMD]", self._stdout
         with open(self._stdout, self._stdmode) as f:
            f.write("[SHCMD] " + cmd_string + "\n")

      self._out, self._err = execute(cmd_string, self._stdout, self._stderr, self._stdin, self._stdmode)

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

