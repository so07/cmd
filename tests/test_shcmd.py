import os
from shcmd.shcmd import shcmd

import random
import string


def get_random_string(length=10):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x


def test_import():
    import shcmd
    from shcmd import shcmd
    from shcmd.shcmd import shcmd
    from shcmd.shcmd import execute


def test_touch(tmpdir):

    filename = "file"

    touch = shcmd("touch")
    touch += os.path.join(tmpdir, filename)

    touch()

    assert os.listdir(tmpdir) == [filename]


def test_str():
    assert str(shcmd("test this command")) == "test this command"


class TestTouch:

    filename = "file"

    def _touch_command(self, path):

        c = shcmd("touch")
        c += os.path.join(path, TestTouch.filename)

        return c

    def test_touch_call(self, tmpdir):

        self._touch_command(tmpdir)()

        assert os.listdir(tmpdir) == [TestTouch.filename]

    def test_touch_execute(self, tmpdir):

        self._touch_command(tmpdir).execute()

        assert os.listdir(tmpdir) == [TestTouch.filename]

    def test_touch_add(self, tmpdir):

        c = self._touch_command(tmpdir)
        c += os.path.join(tmpdir, "another_file")

        c()

        assert os.listdir(tmpdir) == [TestTouch.filename, "another_file"]

    def test_touch_sub(self, tmpdir):

        c = shcmd(os.path.join(tmpdir, TestTouch.filename))
        c -= "touch"

        c()

        assert os.listdir(tmpdir) == [TestTouch.filename]

    def test_dry_run(self, tmpdir):

        c = shcmd("touch", debug=True)
        c += os.path.join(tmpdir, TestTouch.filename)

        c()

        assert os.listdir(tmpdir) == []

    def test_touch_ls(self, tmpdir):

        self._touch_command(tmpdir)()

        assert shcmd("ls " + str(tmpdir))()[0] == TestTouch.filename

    def test_touch_ls_output(self, tmpdir):

        self._touch_command(tmpdir)()

        ls = shcmd("ls " + str(tmpdir))
        ls()

        assert ls.output() == TestTouch.filename
        assert ls.error() == ""

    def test_touch_ls_error(self, tmpdir):

        self._touch_command(tmpdir)()

        ls = shcmd("ls " + get_random_string())
        ls()

        assert ls.error() == ""


def test_execute(tmpdir):

    from shcmd.shcmd import execute

    filename = "file"

    execute("touch " + os.path.join(tmpdir, filename))

    assert os.listdir(tmpdir) == [filename]


def test_is_error_true():

    _, _, error_code = shcmd(get_random_string())()

    assert error_code != 0


def test_is_error_false():

    _, _, error_code = shcmd("ls")()

    assert error_code == 0
