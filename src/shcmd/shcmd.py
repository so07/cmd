#!/usr/bin/env python3
"""
shcmd module
"""

import subprocess
import io

from contextlib import closing

from itertools import zip_longest

__all__ = ["execute", "shcmd"]


def _poll(proc, stdout, stderr, stdmode, silent=False):

    # init stdout
    stdout_iterator = iter(proc.stdout.readline, b"")

    if stdout:
        stdout_context = open(stdout, stdmode)
    else:
        stdout_context = closing(io.StringIO())

    stdout_save = ""

    # init stderr
    if proc.stderr and proc.stdout != proc.stderr:
        stderr_iterator = iter(proc.stderr.readline, b"")
    else:
        # empty iterator
        stderr_iterator = iter([])

    if stderr and stderr != stdout:
        stderr_context = open(stderr, stdmode)
    else:
        stderr_context = closing(io.StringIO())

    stderr_save = ""

    # open contexts for stdout and stderr
    with stdout_context as fo_cont, stderr_context as fe_cont:

        for ito, ite in zip_longest(stdout_iterator, stderr_iterator):

            if ito:
                if not silent:
                    print(ito.decode("utf-8"), end="", flush=True)
                fo_cont.write(ito.decode("utf-8"))
                fo_cont.flush()
                stdout_save += ito.decode("utf-8")

            if ite:
                if not silent:
                    print(ite.decode("utf-8"), end="", flush=True)
                fe_cont.write(ite.decode("utf-8"))
                fe_cont.flush()
                stderr_save += ite.decode("utf-8")

    return stdout_save.strip(), stderr_save.strip()


def execute(command, stdout=None, stderr=None, stdin=None, stdmode="a", silent=False):
    """execute command in a shell"""

    proc = subprocess.Popen(
        command,
        # stdin  = subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )

    _out, _err = _poll(proc, stdout, stderr, stdmode, silent)

    _out2, _err2 = proc.communicate()

    if _out2:
        _out += _out2

    if _err2:
        _err += _err2

    return _out, _err, proc.returncode


class shcmd:
    """shcmd Class to invoke command in a shell from python scripts"""

    def __init__(
        self,
        command,
        stdout=None,
        stderr=None,
        stdin=None,
        msg=None,
        append=False,
        silent=False,
        verbose=False,
        debug=False,
    ):

        self._cmd = [command]

        self._stdout = stdout
        self._stderr = stderr
        self._stdin = stdin

        self._msg = msg

        self._append = append
        self._silent = silent
        self._verbose = verbose
        self._debug = debug

        self._out = None
        self._err = None

        self._stdmode = "w"
        if self._append:
            self._stdmode = "a"

        self._errorcode = 0

    def __str__(self):
        return str(" ".join(self._cmd))

    def __call__(self):
        return self.execute()

    def __add__(self, option):
        self._cmd.append(option)
        return self

    def __sub__(self, option):
        self._cmd.insert(0, option)
        return self

    def execute(self):
        """execute command and returns output, error and error code"""

        cmd_string = " ".join(self._cmd)

        if not self._silent:
            if self._verbose and self._stdout:
                print("[SHCMD] STDOUT", self._stdout)
            if self._msg:
                print("[SHCMD]", self._msg)
            print("[SHCMD]", cmd_string)

        if self._debug:
            return

        if self._stdout:
            with open(self._stdout, self._stdmode) as fop:
                if self._msg:
                    print("[SHCMD]", self._msg, file=fop)
                print("[SHCMD]", cmd_string, file=fop)

        # NB: stdmode always 'a' calling execute.
        # Thus command string in stdout file
        self._out, self._err, self._errorcode = execute(
            cmd_string, self._stdout, self._stderr, self._stdin, "a", self._silent
        )

        return self._out, self._err, self._errorcode

    def output(self):
        """return command output"""
        return self._out

    def error(self):
        """return command error"""
        return self._err

    def stdout(self):
        """return command stdout"""
        return self._stdout

    def stderr(self):
        """return command stderr"""
        return self._stderr

    def stdin(self):
        """return command stdinp"""
        return self._stdin

    def is_error(self):
        """return true if command ends successfully and false otherwise"""
        if self._errorcode:
            return True
        return False
