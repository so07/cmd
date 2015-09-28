#!/usr/bin/env python
from shcmd import shcmd

def main():
   cmd = " ".join(sys.argv[1:])
   shcmd(cmd)()

def debug():
   #shcmd(sys.argv[1])()

   #c = shcmd("ls;sleep 1;ls -l 1;sleep 1;ls shcmd.py; sleep 10")
   #c = shcmd("ls;sleep 1;ls -l 1;sleep 1;ls shcmd.py; sleep 10", stdout = 'log')
   #c = shcmd("ls;sleep 1;ls -l 1;sleep 1;ls shcmd.py; sleep 10", stdout = 'log', stderr = 'err')

   c = shcmd("ls -l ", msg = 'Now a message for this command!')

   #c = shcmd("watch -n 1 cat shcmd.py; sleep 5")
   c = shcmd("cat shcmd.py; sleep 5")
   c = shcmd("cat shcmd.py; sleep 3; echo OK ; sleep 3 ; cat shcmd.py")
   #c = shcmd(">&2 echo error ; echo output1 ; echo output2 ", stdout='the_output', stderr='the_error', msg = "message")

   c()

   #shcmd("ls", msg = 'Another message')()


if __name__ == "__main__":
   debug()
   #main()

