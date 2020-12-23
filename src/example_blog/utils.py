"""Utils"""
import asyncio
import contextlib
import os
from functools import partial
from os import PathLike
from typing import Any, TypeVar, Union

from pydantic import BaseModel as SchemaModel

from example_blog.models import BaseModel

ModelType = TypeVar('ModelType', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=SchemaModel)
UpdateSchema = TypeVar('UpdateSchema', bound=SchemaModel)


async def run_in_executor(func, *args, **kwargs) -> Any:
    """
    如果自定义 executor 请在 kwargs 中传入。
    :param func:
    :param kwargs:
        : kwargs func 的字典参数
        : executor 自定义 executor
    :return:
    """
    executor = kwargs.pop('executor', None)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, partial(func, *args, **kwargs))


@contextlib.contextmanager
def chdir(path: Union[str, PathLike]):
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)
