"""
ABSFUYU
-------
A small collection of code

LINKS
-----
- Home page: https://pypi.org/project/absfuyu/
- Documentation: https://absolutewinter.github.io/absfuyu/

USAGE
-----
`import absfuyu`

`absfuyu.help()`
"""


__title__ = "absfuyu"
__author__ = "AbsoluteWinter"
__license__ = "MIT License"
__all__ = [
    # default
    "calculation", "data", "generator",
    "strings", "util", "lists",
    # extra
    "fibonacci", "obfuscator", "sort", "fun",
    "stats", "pkg_data", "extra", "dicts",
    "game", "tools", "extensions",
    # config
    "config",
    # Other
    # "help", "pry", "version",
    # "everything",
]

# default function
from .help import *
from .pry import *
from .version import __version__
from .version import check_for_update


# default module
from . import calculation as cal
from . import data
from . import generator as gen
from . import lists
from . import strings
from . import util


# config
# from . import config as __config
# __config.welcome()


# luckgod
from . import code_red as __red
__red.luckgod()