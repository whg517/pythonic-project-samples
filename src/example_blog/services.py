"""Service"""
import math
from typing import Dict, Generic, List

from example_blog.db import SessionFactory
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from example_blog.dao import BaseDAO, UserDAO, ArticleDAO
from example_blog.exceptions import AuthException
from example_blog.models import User
from example_blog.schemas import CreateUserSchema, UpdateUserSchema
from example_blog.utils import (CreateSchema, ModelType, UpdateSchema,
                                create_access_token, verify_credential,
                                verify_password)


class Paginator:
    _MAX_PAGE_SIZE = 3

    def __init__(self, dao: BaseDAO):
        self.dao = dao


class BaseService(Generic[ModelType, CreateSchema, UpdateSchema]):
    dao: BaseDAO

    def get(self, session: Session, size=0, page=10) -> Dict:
        """"""
        objs = self.dao.get(session)
        objs_dict = jsonable_encoder(objs)
        return {
            'content': objs_dict
        }

    def total(self, session: Session) -> int:
        return self.dao.count(session)

    def get_by_id(self, session: Session, pk: int) -> ModelType:
        """Get by id"""
        return self.dao.get_by_id(session, pk)

    def create(self, session: Session, obj_in: CreateSchema) -> ModelType:
        """Create a object"""
        return self.dao.create(session, obj_in)

    def patch(self, session: Session, pk: int, obj_in: UpdateSchema) -> None:
        """Update"""
        return self.dao.patch(session, pk, obj_in)

    def delete(self, session: Session, pk: int) -> None:
        """Delete a object"""
        return self.dao.delete(session, pk)


class UserService(BaseService[User, CreateUserSchema, UpdateUserSchema]):
    dao = UserDAO()

    def auth_for_access_token(self, session: Session, username: str, password: str) -> Dict:
        """使用用户名密码验证，并返回 access_token"""
        user = self.dao.get_by_name(session, username)
        if user and verify_password(password, user.password):
            return {
                'access_token': create_access_token({'sub': user.name}),
                'token_type': 'bearer'
            }
        else:
            raise AuthException()

    def get_current_user(self, session: Session, token: str):
        """通过 jwt token 验证并获取 user"""
        username = verify_credential(token)
        return self.dao.get_by_name(session, username)


class ArticleService(BaseService):
    dao = ArticleDAO()

    def __init__(self):
        pass

    def __call__(self, request: Request) -> 'ArticleService':
        return self


user_service = UserService()
