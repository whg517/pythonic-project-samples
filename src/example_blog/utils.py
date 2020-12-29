"""Utils"""

import contextlib
import os
from os import PathLike
from typing import Union


@contextlib.contextmanager
def chdir(path: Union[str, PathLike]):
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)
