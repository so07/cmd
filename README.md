# shcmd

[![Build Status](https://travis-ci.com/so07/shcmd.svg?token=CFvNdbNXiYKX1TcDAvWp&branch=master)](https://travis-ci.com/so07/shcmd)
[![Coverage Status](https://coveralls.io/repos/github/so07/shcmd/badge.svg?branch=master)](https://coveralls.io/github/so07/shcmd?branch=master)

Invoke command in shell.

## Usage

To execute a command in a python script write the following python code in a `script.py` file

```python
from shcmd.shcmd import shcmd

clone = shcmd("git clone https://github.com/so07/shcmd.git")

clone()
```

When execute the `script.py` file
```
$ python script.py
[SHCMD] git clone https://github.com/so07/shcmd.git
Cloning into 'shcmd'...
```

Another example is the following
```python
from shcmd.shcmd import shcmd

ls = shcmd("ls")
ls += "shcmd"

ls()
```

This is the output of the command above
```
[SHCMD] ls shcmd
CHANGELOG.md
README.md
setup.py
src
tests
```
