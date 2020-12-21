
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from example_blog.services import user_service


def get_db(request: Request) -> Session:
    return request.state.db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return user_service.get_current_user(session, token)


class CommonQueryParams:
    def __init__(
            self,
            # filters: Optional[List[str]] = Query(None, title='Filters', description='key=value'),
            # sorts: Optional[List[str]] = Query(None, title='Filters', description='key,desc'),
            page: int = 1,
            size: int = 3

    ):
        self.page = page
        self.size = size
        # self.filters = filters
        # self.sorts = sorts
