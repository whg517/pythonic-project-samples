from fastapi import APIRouter, FastAPI

from example_blog.views import article


def router_v1():
    router = APIRouter()
    router.include_router(article.router, tags=['Article'])
    return router


def init_routers(app: FastAPI):
    app.include_router(router_v1(), prefix='/api/v1', tags=['v1'])
