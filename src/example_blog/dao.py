from typing import Generic, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from example_blog.models import Article
from example_blog.utils import CreateSchema, ModelType, UpdateSchema


class BaseDAO(Generic[ModelType, CreateSchema, UpdateSchema]):
    model: ModelType

    def get(self, session: Session, offset=0, limit=10) -> List[ModelType]:
        result = session.query(self.model).offset(offset).limit(limit).all()
        return result

    def get_by_id(self, session: Session, pk: int, ) -> ModelType:
        return session.query(self.model).get(pk)

    def create(self, session: Session, obj_in: CreateSchema) -> ModelType:
        """Create"""
        obj = self.model(**jsonable_encoder(obj_in))
        session.add(obj)
        session.commit()
        return obj

    def patch(self, session: Session, pk: int, obj_in: UpdateSchema) -> ModelType:
        """Patch"""
        obj = self.get_by_id(session, pk)
        update_data = obj_in.dict(exclude_unset=True)
        for key, val in update_data.items():
            setattr(obj, key, val)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, pk: int) -> None:
        """Delete"""
        obj = self.get_by_id(session, pk)
        session.delete(obj)
        session.commit()

    def count(self, session: Session):
        return session.query(self.model).count()


class ArticleDAO(BaseDAO):
    model = Article
