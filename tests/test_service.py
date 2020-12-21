import pytest

from example_blog.services import UserService


class TestUserService:

    @pytest.fixture()
    def service(self):
        yield UserService()

    @pytest.mark.asyncio
    async def test_get(self, service):
        res = await service.get()
        print(res)
