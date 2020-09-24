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

        c = shcmd("touch")
        c += os.path.join(path, TestTouch.filename)

        return c

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

        c = self._touch_command(tmpdir)
        c += os.path.join(tmpdir, "another_file")

        c()

        assert os.listdir(tmpdir) == [TestTouch.filename, "another_file"]

    def test_touch_sub(self, tmpdir):
        """test for shcmd sub method"""

        c = shcmd(os.path.join(tmpdir, TestTouch.filename))
        c -= "touch"

        c()

        assert os.listdir(tmpdir) == [TestTouch.filename]

    def test_debug(self, tmpdir):
        """test for shcmd debug option"""

        c = shcmd("touch", debug=True)
        c += os.path.join(tmpdir, TestTouch.filename)

        c()

        assert os.listdir(tmpdir) == []

    def test_touch_ls(self, tmpdir):
        """test ls command"""

        self._touch_command(tmpdir)()

        assert shcmd("ls " + str(tmpdir))()[0] == TestTouch.filename

    def test_touch_ls_output(self, tmpdir):
        """test shcmd output and error methods with touch and ls commands"""

        self._touch_command(tmpdir)()

        ls = shcmd("ls " + str(tmpdir))
        ls()

        assert ls.output() == TestTouch.filename
        assert ls.error() == ""

    def test_touch_ls_error(self, tmpdir):
        """test shcmd error method with touch and ls commands"""

        self._touch_command(tmpdir)()

        ls = shcmd("ls " + get_random_string())
        ls()

        assert ls.error() == ""


def test_execute(tmpdir):
    """test shcmd execute function"""

    from shcmd.shcmd import execute

    filename = "file"

    execute("touch " + os.path.join(tmpdir, filename))

    assert os.listdir(tmpdir) == [filename]


def test_is_error_true():
    """test for not valid shcmd error code"""

    _, _, error_code = shcmd(get_random_string())()

    assert error_code != 0


def test_is_error_false():
    """test for valid shcmd error code"""

    _, _, error_code = shcmd("ls")()

    assert error_code == 0
