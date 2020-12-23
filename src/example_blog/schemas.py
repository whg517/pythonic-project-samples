from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr


class InDBMixin(BaseModel):
    id: int

    class Config:
        orm_mode = True


class BaseArticle(BaseModel):
    title: constr(max_length=500)
    body: Optional[str] = None


class ArticleSchema(BaseArticle, InDBMixin):
    create_time: datetime
    update_time: datetime


class CreateArticleSchema(BaseArticle):
    pass


class UpdateArticleSchema(BaseArticle):
    title: Optional[constr(max_length=500)] = None
