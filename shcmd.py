#!/usr/bin/env python
import sys
import os
import subprocess
import StringIO

from contextlib import closing

from itertools import izip_longest as zip

__all__ = ['execute', 'shcmd']


def _poll(p, stdout, stderr, stdmode, silent=False):

   # init stdout
   stdout_iterator = iter(p.stdout.readline, b"")

   if stdout:
      stdout_context = open(stdout, stdmode)
   else:
      stdout_context = closing(StringIO.StringIO())

   stdout_save = ''

   # init stderr
   if p.stderr and p.stdout != p.stderr:
      stderr_iterator = iter(p.stderr.readline, b"")
   else:
      # empty iterator
      stderr_iterator = iter([])

   if stderr and stderr != stdout:
      stderr_context = open(stderr, stdmode)
   else:
      stderr_context = closing(StringIO.StringIO())

   stderr_save = ''

   # open contexts for stdout and stderr
   with stdout_context as fo, stderr_context as fe:

      for o, e in zip(stdout_iterator, stderr_iterator):

           if o:
              if not silent:
                 print o,
              fo.write(o)
              fo.flush()
              stdout_save += o

           if e:
              if not silent:
                 print e,
              fe.write(e)
              fe.flush()
              stderr_save += e

   return stdout_save.strip(), stderr_save.strip()


def execute (command, stdout=None, stderr=None, stdin=None, stdmode='a', silent=False):

   p = subprocess.Popen(command,
                        #stdin  = subprocess.PIPE,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.STDOUT,
                        shell=True)

   _out, _err = _poll(p, stdout, stderr, stdmode, silent)

   _out2, _err2 = p.communicate()

   if _out2:
      _out += _out2

   if _err2:
      _err += _err2

   return _out, _err, p.returncode


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

      cmd_string = " ".join( self._cmd )

      if not self._silent:
         if self._verbose and self._stdout:
             print "[SHCMD] STDOUT", self._stdout
         if self._msg:
             print "[SHCMD]", self._msg
         print "[SHCMD]", cmd_string

      if self._debug:
         return

      if self._stdout:
         with open(self._stdout, self._stdmode) as f:
            if self._msg:
                print >> f, "[SHCMD]", self._msg
            print >> f, "[SHCMD]", cmd_string

      # NB stdmode always 'a' calling execute. Thus command string in stdout file
      self._out, self._err, self._errorcode = execute(cmd_string, self._stdout, self._stderr, self._stdin, 'a', self._silent)

      return self._out, self._err, self._errorcode


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

