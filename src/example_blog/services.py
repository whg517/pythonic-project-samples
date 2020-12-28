"""Service"""
from typing import Generic, List

from sqlalchemy.orm import Session

from example_blog.dao import ArticleDAO, BaseDAO
from example_blog.models import Article
from example_blog.schemas import CreateSchema, ModelType, UpdateSchema


class BaseService(Generic[ModelType, CreateSchema, UpdateSchema]):
    dao: BaseDAO

    def get(self, session: Session, offset=0, limit=10) -> List[ModelType]:
        """"""
        return self.dao.get(session, offset=offset, limit=limit)

    def total(self, session: Session) -> int:
        return self.dao.count(session)

    def get_by_id(self, session: Session, pk: int) -> ModelType:
        """Get by id"""
        return self.dao.get_by_id(session, pk)

    def create(self, session: Session, obj_in: CreateSchema) -> ModelType:
        """Create a object"""
        return self.dao.create(session, obj_in)

    def patch(self, session: Session, pk: int, obj_in: UpdateSchema) -> ModelType:
        """Update"""
        return self.dao.patch(session, pk, obj_in)

    def delete(self, session: Session, pk: int) -> None:
        """Delete a object"""
        return self.dao.delete(session, pk)


class ArticleService(BaseService[Article, CreateSchema, UpdateSchema]):
    dao = ArticleDAO()
