import os
import threading

import pytest

from example_blog.utils import chdir, run_in_executor


@pytest.mark.asyncio
async def test_run_in_executor():
    _id = threading.get_ident()

    def f():
        return threading.get_ident()

    res = await run_in_executor(f)
    assert isinstance(res, int)
    assert res != _id


def test_chdir():
    path = '/tmp'
    cwd = os.getcwd()
    with chdir(path):
        assert path == os.getcwd()
    assert cwd == os.getcwd()
