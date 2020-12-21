from typing import Callable

from fastapi import FastAPI, Request, Response

from example_blog.db import SessionFactory


async def db_session_middleware(request: Request, call_next: Callable) -> Response:
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionFactory()
        response = await call_next(request)
    finally:
        request.state.db.close()

    return response


def init_middleware(app: FastAPI) -> None:
    app.middleware('http')(db_session_middleware)
