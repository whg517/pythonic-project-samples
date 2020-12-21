import functools
from typing import Optional
import inspect

from example_blog.dependencies import get_db
from example_blog.services import ArticleService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


def injection_service(service: Optional[Depends] = None):
    def _decorator(func):
        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        sig = inspect.signature(__wrapper)
        print(sig.parameters)
        return __wrapper

    return _decorator


@router.get('/articles')
@injection_service(Depends(ArticleService()))
def get(
        service,
        session: Session = Depends(get_db),
):
    # print(id(service))
    # resp = service.get(session)
    # return resp
    return {}
