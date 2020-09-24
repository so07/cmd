"""
unit tests for cli to shcmd module
"""

import pytest


from shcmd.main import main


def test_main(capsys):
    """test for main function"""

    with pytest.raises(SystemExit):
        main()

    out, err = capsys.readouterr()

    assert out == ""
    assert (
        err
        == "usage: shcmd [-h] [--version] -c COMMAND [-o STDOUT] [-e STDERR] [-i STDINP]\n             [-m MESSAGE] [-a] [-s] [-v] [-d]\nshcmd: error: the following arguments are required: -c/--command\n"
    )
