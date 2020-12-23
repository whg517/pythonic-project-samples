import pytest

from example_blog.dao import ArticleDAO
from example_blog.models import Article
from example_blog.schemas import CreateArticleSchema, UpdateArticleSchema


class TestArticle:

    @pytest.fixture()
    def dao(self, init_article):
        yield ArticleDAO()

    def test_get(self, dao, session):
        users = dao.get(session)
        assert len(users) == 3
        users = dao.get(session, limit=2)
        assert len(users) == 2
        users = dao.get(session, offset=4)
        assert not users

    def test_get_by_id(self, dao, session):
        user = dao.get_by_id(session, 1)
        assert user.id == 1

    def test_create(self, dao, session):
        origin_count = session.query(dao.model).count()
        obj_in = CreateArticleSchema(title='test')
        dao.create(session, obj_in)
        count = session.query(dao.model).count()
        assert origin_count + 1 == count

    def test_patch(self, dao, session):
        obj: Article = session.query(dao.model).first()
        body = obj.body
        obj_in = UpdateArticleSchema(body='test')
        updated_obj: Article = dao.patch(session, obj.id, obj_in)
        assert body != updated_obj.body

    def test_delete(self, dao, session):
        origin_count = session.query(dao.model).count()
        dao.delete(session, 1)
        count = session.query(dao.model).count()
        assert origin_count - 1 == count

    def test_count(self, dao, session):
        count = dao.count(session)
        assert count == 3
