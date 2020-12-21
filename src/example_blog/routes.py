from fastapi import APIRouter, Depends, FastAPI

from example_blog.dependencies import get_current_user
from example_blog.views import article, auth, user


def router_v1():
    router = APIRouter(
        # dependencies=[Depends(get_current_user)]
    )    # Add auth
    # router.include_router(user.router, tags=['Users'])
    router.include_router(article.router, tags=['Article'])
    return router


def init_routers(app: FastAPI):
    app.include_router(auth.router)
    app.include_router(router_v1(), prefix='/api/v1', tags=['v1'])
