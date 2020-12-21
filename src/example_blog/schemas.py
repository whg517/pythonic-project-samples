from datetime import datetime

from pydantic import BaseModel, constr


class InDBMixin(BaseModel):
    id: int

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    name: constr(max_length=500)
    password: constr(max_length=1024)
    create_time: datetime = None


class UserSchema(BaseUser, InDBMixin):
    name: constr(max_length=500)
    password: constr(max_length=1024)
    create_time: datetime = None


class CreateUserSchema(BaseUser):
    pass


class UpdateUserSchema(BaseUser):
    pass
