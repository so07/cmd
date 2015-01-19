#!/usr/bin/python
import sys
import subprocess

__all__ = ['exe', 'output', 'error', 'stdout', 'stderr']

def _poll(p):
   while True:
      nextline = p.stdout.readline()
      if nextline == '' and p.poll() != None:
         break
      sys.stdout.write(nextline)
      sys.stdout.flush()

def exe(command, stdout=None, stderr=None, stdin=None):

   p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

   _poll(p)

   out, err = p.communicate()

   return out, err


class cmd:

   def __init__(self, command, stdout=None, stderr=None, stdin=None, debug=False):
      self._cmd = [command]

      self._stdout = stdout
      self._stderr = stderr
      self._stdin  = stdin

      self._debug  = debug

      self._out = None
      self._err = None

   def __str__(self):
      return str( " ".join(self._cmd) )

   def __call__(self, **kwargs):
      return self.exe(**kwargs)

   def __add__ (self, option):
      self._cmd.append(option)
      return self
   def __sub__ (self, option):
      self._cmd.insert(0, option)
      return self


   def exe(self, stdout=None, stderr=None, stdin=None):

      s = " ".join( self._cmd )

      if self._debug:
         print s
         return

      self._out, self._err = exe(s, stdout, stderr, stdin)

      #if self._err :
      #    self._write_stderr(stderr)

      if self._err:
         print self._err

      self._write_stdout(stdout)

      return self._out


   def _write_stdout(self, stdout=None):
       if not stdout:
           stdout = self._stdout
       if not stdout:
          return
       with open(stdout, 'a') as f:
          print >> f, self._out

   def _write_stderr(self, stderr=None):
       print "[CMD] ERROR"
       print self._err
       if not stderr:
           stderr = self._stderr
       if not stderr:
           return
       with open(stderr, 'a') as f:
          print >> f, self._err


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


def main():

   a = cmd("ls")
   print a
   a()

   print a.output()

   a += '-l'
   print a()


   print exe('ls')[0]


   print ">>> debug mode"
   b = cmd('ls', debug = True)
   b()


if __name__ == "__main__":
   #import doctest
   #doctest.testmod()
   main()

