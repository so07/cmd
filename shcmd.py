#!/usr/bin/env python
import sys
import subprocess

__all__ = ['exe', 'shcmd']

def _polling(p, stdout, stderr):
   if stdout:
      fp = open(stdout, 'w')
   save_stdout = ''
   while True:
      nextline = p.stdout.readline()
      save_stdout += nextline
      if nextline == '' and p.poll() != None:
         break
      sys.stdout.write(nextline)
      sys.stdout.flush()
      if stdout:
         print >> fp, nextline,
         fp.flush()
   return save_stdout

def exe(command, stdout=None, stderr=None, stdin=None):

   p = subprocess.Popen(command,
                        stdin  = subprocess.PIPE,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE,
                        shell=True)

   out = _polling(p, stdout, stderr)

   out2, err = p.communicate()

   out += out2

   return out, err


class shcmd:

   def __init__(self, command,
                      stdout=None,
                      stderr=None,
                      stdin=None,
                      debug=False):

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

      print s
      if self._debug:
         return

      self._out, self._err = exe(s, self._stdout, self._stderr, self._stdin)

      self._write_stderr(stderr)

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
       if not self._err : return
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



if __name__ == "__main__":

   #shcmd(sys.argv[1])()

   c = shcmd("ls -l; sleep 30", stdout = 'log')

   c()

