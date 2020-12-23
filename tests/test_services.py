import pytest

from example_blog.schemas import CreateArticleSchema, UpdateArticleSchema
from example_blog.services import ArticleService


class TestArticleService:

    @pytest.fixture()
    def service(self, init_article):
        yield ArticleService()

    def test_get(self, service, session):
        objs = service.get(session)
        assert len(objs) == 3
        objs = service.get(session, limit=2)
        assert len(objs) == 2
        objs = service.get(session, offset=5)
        assert not objs

    def test_total(self, service, session):
        total = service.total(session)
        assert total == 3

    def test_by_id(self, service, session):
        __obj = session.query(service.dao.model).first()
        obj = service.get_by_id(session, __obj.id)
        assert obj.id == __obj.id

    def test_create(self, service, session):
        origin_count = service.total(session)
        obj_in = CreateArticleSchema(title='test')
        service.create(session, obj_in)
        count = service.total(session)
        assert origin_count + 1 == count

    def test_patch(self, service, session):
        origin_obj = session.query(service.dao.model).first()
        body = origin_obj.body
        obj_in = UpdateArticleSchema(body='test')
        obj = service.patch(session, origin_obj.id, obj_in)
        assert body != obj.body

    def test_delete(self, service, session):
        origin_count = service.total(session)
        obj = session.query(service.dao.model).first()
        service.delete(session, obj.id)
        count = service.total(session)
        assert origin_count - 1 == count
