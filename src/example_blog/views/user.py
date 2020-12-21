import math
from typing import List, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from example_blog.dependencies import CommonQueryParams, get_db
from example_blog.schemas import CreateUserSchema, UpdateUserSchema, UserSchema
from example_blog.services import UserService

router = APIRouter()

user_service = UserService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_service(request: Request):
    return request


"""
如何在请求进来的时候自动注入 service ?
"""


@router.get('/users')
def get(
        session: Session = Depends(get_db),  # function depend
        commons: CommonQueryParams = Depends(),  # Class Depend
):
    objs = user_service.get(session)
    return {
        'content': objs,
    }


@router.get('/users/{pk}', response_model=UserSchema)
async def get_by_id(
        pk: int,
        session: Session = Depends(get_db),
):
    resp = user_service.get_by_id(session, pk)
    return resp


@router.post('/users', response_model=UserSchema)
def create(
        obj_in: CreateUserSchema,
        session: Session = Depends(get_db),
):
    return user_service.create(session, obj_in)


@router.patch('/users/{pk}')
def patch(
        pk: int,
        obj_in: UpdateUserSchema,
        session: Session = Depends(get_db),
):
    return user_service.patch(session, pk, obj_in)


@router.delete('/users/{pk}')
def delete(
        pk: int,
        session: Session = Depends(get_db),
):
    return user_service.delete(session, pk)
