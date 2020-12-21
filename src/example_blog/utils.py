"""Utils"""
import asyncio
from datetime import datetime, timedelta
from functools import partial
from typing import Any, Optional, TypeVar

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel as SchemaModel

from example_blog.config import settings
from example_blog.exceptions import CredentialsException
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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """使用明文和密文验证是否一致"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    """create jwt token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_credential(token: str) -> str:
    """verify jwt token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
    except JWTError:
        raise CredentialsException()
    return username
