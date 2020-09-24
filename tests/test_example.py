def test_example():
    """test for shcmd example usage"""

    from shcmd.shcmd import shcmd

    ls = shcmd("ls")

    ls()
