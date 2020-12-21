from typing import Any, Dict, Optional

from fastapi import HTTPException
from starlette import status


class ObjectNotFound(HTTPException):

    def __init__(self):
        super().__init__(status.HTTP_404_NOT_FOUND, 'Object not found.')


class AuthException(HTTPException):
    def __init__(self, detail='Incorrect username or password.'):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers={"WWW-Authenticate": "Bearer"})


class CredentialsException(AuthException):
    def __init__(self, detail='Incorrect username or password.'):
        super().__init__(detail)
