#!/usr/bin/env python
import sys
import os
import subprocess
import threading
import Queue


__all__ = ['exe', 'shcmd']


class AsynchronousFileReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue
 
    def run(self):
        '''Read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)
 
    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()


def _poll(p, stdout, stderr):

   if stdout:
      if os.path.isfile(stdout):
         os.remove(stdout)
      op = open(stdout, 'a')
   if stderr:
      if os.path.isfile(stderr):
         os.remove(stderr)
      ep = open(stderr, 'a')

   # Launch the asynchronous readers of the process' stdout and stderr.
   stdout_queue = Queue.Queue()
   stdout_reader = AsynchronousFileReader(p.stdout, stdout_queue)
   stdout_reader.start()
   stderr_queue = Queue.Queue()
   stderr_reader = AsynchronousFileReader(p.stderr, stderr_queue)
   stderr_reader.start()

   _out = ''
   _err = ''

   # Check the queues if we received some output (until there is nothing more to get).
   while not stdout_reader.eof() or not stderr_reader.eof():

       # receive from standard output.
       while not stdout_queue.empty():
           line = stdout_queue.get()
           print line,
           _out += line
           if stdout:
              op.write(line)
              op.flush()
 
       # receive from standard error.
       while not stderr_queue.empty():
           line = stderr_queue.get()
           _err += line
           print line,
           if stderr:
              ep.write(line)
              ep.flush()
 
   # join threads we've started.
   stdout_reader.join()
   stderr_reader.join()
 
   if stdout:
      op.close()

   if stderr:
      ep.close()

   return _out, _err


def exe(command, stdout=None, stderr=None, stdin=None, merge_outerr=False):

   pipe_out = subprocess.PIPE
   pipe_err = subprocess.PIPE

   if merge_outerr:
       pipe_err = subprocess.STDOUT

   p = subprocess.Popen(command,
                        stdin  = subprocess.PIPE,
                        stdout = pipe_out,
                        stderr = pipe_err,
                        shell=True)

   poll_out, poll_err = _poll(p, stdout, stderr)
   comm_out, comm_err = p.communicate()

   _out = poll_out + comm_out
   _err = poll_err + comm_err

   return _out, _err


class shcmd:

   def __init__(self, command,
                      stdout = None, stderr = None, stdin = None,
                      msg = None,
                      debug = False):

      self._cmd = [command]

      self._stdout = stdout
      self._stderr = stderr
      self._stdin  = stdin

      self._msg    = msg

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

      if self._msg:
          print "[SHCMD]", self._msg

      s = " ".join( self._cmd )

      print s
      if self._debug:
         return

      self._out, self._err = exe(s, self._stdout, self._stderr, self._stdin)

      #self._write_stderr(stderr)
      #self._write_stdout(stdout)

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
       print "[CMD] STDERR :", self._err
       #print self._err
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
   cmd = " ".join(sys.argv[1:])
   shcmd(cmd)()

def debug():
   #shcmd(sys.argv[1])()

   #c = shcmd("ls;sleep 1;ls -l 1;sleep 1;ls shcmd.py; sleep 10")
   #c = shcmd("ls;sleep 1;ls -l 1;sleep 1;ls shcmd.py; sleep 10", stdout = 'log')
   #c = shcmd("ls;sleep 1;ls -l 1;sleep 1;ls shcmd.py; sleep 10", stdout = 'log', stderr = 'err')

   c = shcmd("ls -l ", msg = 'Now a message for this command!')

   c()

   #shcmd("ls", msg = 'Another message')()


if __name__ == "__main__":
   #debug()
   main()

