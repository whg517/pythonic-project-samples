import pytest

from example_blog.dao import UserDAO


class TestUser:

    @pytest.fixture()
    def user_dao(self):
        yield UserDAO()

    def test_get(self, user_dao):
        users = user_dao.get()
        print(users)

    def test_get_by_id(self, user_dao):
        user = user_dao.get()
        assert user.id == 1
