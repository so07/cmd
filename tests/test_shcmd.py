"""
unit tests for shcmd module
"""
import os
import random
import string

from shcmd.shcmd import shcmd


def get_random_string(length=10):
    """return random string of given length"""
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def test_import():
    """test import module"""
    import shcmd
    from shcmd import shcmd
    from shcmd.shcmd import shcmd
    from shcmd.shcmd import execute


def test_str():
    """test command conversion to string"""
    assert str(shcmd("test this command")) == "test this command"


class TestTouch:
    """class for testing shcmd functionality with usage of touch command"""

    filename = "file"

    @staticmethod
    def _touch_command(path):
        """return shcmd instance for touch a file in the path directory"""

        cmd = shcmd("touch")
        cmd += os.path.join(path, TestTouch.filename)

        return cmd

    def test_touch_call(self, tmpdir):
        """test for shcmd call method"""

        self._touch_command(tmpdir)()

        assert os.listdir(tmpdir) == [TestTouch.filename]

    def test_touch_execute(self, tmpdir):
        """test for shcmd execute method"""

        self._touch_command(tmpdir).execute()

        assert os.listdir(tmpdir) == [TestTouch.filename]

    def test_touch_add(self, tmpdir):
        """test for shcmd add method"""

        cmd = self._touch_command(tmpdir)
        cmd += os.path.join(tmpdir, "another_file")

        cmd()

        assert os.listdir(tmpdir) == [TestTouch.filename, "another_file"]

    def test_touch_sub(self, tmpdir):
        """test for shcmd sub method"""

        cmd = shcmd(os.path.join(tmpdir, TestTouch.filename))
        cmd -= "touch"

        cmd()

        assert os.listdir(tmpdir) == [TestTouch.filename]

    def test_debug(self, tmpdir):
        """test for shcmd debug option"""

        cmd = shcmd("touch", debug=True)
        cmd += os.path.join(tmpdir, TestTouch.filename)

        cmd()

        assert os.listdir(tmpdir) == []

    def test_touch_ls(self, tmpdir):
        """test ls command"""

        self._touch_command(tmpdir)()

        assert shcmd("ls " + str(tmpdir))()[0] == TestTouch.filename

    def test_touch_ls_output(self, tmpdir):
        """test shcmd output and error methods with touch and ls commands"""

        self._touch_command(tmpdir)()

        ls_cmd = shcmd("ls " + str(tmpdir))
        ls_cmd()

        assert ls_cmd.output() == TestTouch.filename
        assert ls_cmd.error() == ""

    def test_touch_ls_error(self, tmpdir):
        """test shcmd error method with touch and ls commands"""

        self._touch_command(tmpdir)()

        ls_cmd = shcmd("ls " + get_random_string())
        ls_cmd()

        assert ls_cmd.error() == ""

    def test_stdout(self, tmpdir):
        """test for shcmd stdout"""

        self._touch_command(tmpdir)()

        file_out = os.path.join(tmpdir, "a" + get_random_string())

        cmd = shcmd("ls -t " + str(tmpdir), stdout=file_out)

        assert not os.path.isfile(file_out)

        cmd()

        assert cmd.stdout() == file_out

        assert os.path.isfile(file_out)

        with open(file_out, "r") as fptr:
            data = fptr.read().strip()

        assert (
            data
            == "[SHCMD] ls -t "
            + str(tmpdir)
            + "\n"
            + os.path.basename(file_out)
            + "\n"
            + TestTouch.filename
        )


def test_execute(tmpdir):
    """test shcmd execute function"""

    from shcmd.shcmd import execute

    filename = "file"

    execute("touch " + os.path.join(tmpdir, filename))

    assert os.listdir(tmpdir) == [filename]


def test_is_error_true():
    """test for not valid shcmd error code"""

    cmd = shcmd(get_random_string())

    _, _, error_code = cmd()

    assert error_code != 0
    assert cmd.is_error()


def test_is_error_false():
    """test for valid shcmd error code"""

    cmd = shcmd("ls")

    _, _, error_code = cmd()

    assert error_code == 0
    assert not cmd.is_error()


def test_stdout(tmpdir):
    """test for shcmd stdout method"""

    file_out = os.path.join(tmpdir, get_random_string())

    cmd = shcmd(get_random_string(), stdout=file_out)

    assert cmd.stdout() == file_out


def test_stderr(tmpdir):
    """test for shcmd stderr method"""

    file_err = os.path.join(tmpdir, get_random_string())

    cmd = shcmd(get_random_string(), stderr=file_err)

    assert cmd.stderr() == file_err


def test_stdinp(tmpdir):
    """test for shcmd stdin method"""

    file_inp = os.path.join(tmpdir, get_random_string())

    cmd = shcmd(get_random_string(), stdin=file_inp)

    assert cmd.stdin() == file_inp


def test_stdout(tmpdir):
    """test for shcmd stdout"""

    msg = "a message"
    file_out = os.path.join(tmpdir, get_random_string())

    cmd = shcmd("touch", msg=msg, stdout=file_out)
    cmd += os.path.join(tmpdir, TestTouch.filename)

    cmd()

    with open(file_out, "r") as fptr:
        data = fptr.read().strip()

    assert data == "[SHCMD] " + msg + "\n[SHCMD] " + str(cmd)


def test_msg(tmpdir):
    """test for shcmd message"""

    msg = "a message"
    file_out = os.path.join(tmpdir, get_random_string())

    cmd = shcmd("touch", msg=msg, stdout=file_out)
    cmd += os.path.join(tmpdir, TestTouch.filename)

    cmd()

    with open(file_out, "r") as fptr:
        data = fptr.read().strip()

    assert data == "[SHCMD] " + msg + "\n[SHCMD] " + str(cmd)


def test_append(tmpdir):
    """test for shcmd append"""

    file_out = os.path.join(tmpdir, get_random_string())

    cmd1 = shcmd("touch", stdout=file_out, append=False)
    cmd1 += os.path.join(tmpdir, TestTouch.filename)

    cmd1()

    cmd2 = shcmd("touch", stdout=file_out, append=True)
    cmd2 += os.path.join(tmpdir, TestTouch.filename)

    cmd2()

    with open(file_out, "r") as fptr:
        data = fptr.read().strip()

    assert data == "[SHCMD] " + str(cmd1) + "\n[SHCMD] " + str(cmd2)

    cmd1()

    with open(file_out, "r") as fptr:
        data = fptr.read().strip()

    assert data == "[SHCMD] " + str(cmd1)
