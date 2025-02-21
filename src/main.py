from typing import List

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.responses import JSONResponse

from src.core.middlewares.auth_middleware import AuthenticationMiddleware, AuthBackend
from src.core.exceptions.base import CustomException
from src.health.routers import health_router

# web domain which can access api
origins = [
    "*",
]


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error
        )
    ]
    return middleware


def init_routers(app_: FastAPI) -> None:
    prefix_router = APIRouter(prefix="/api/v1")
    prefix_router.include_router(health_router)

    app_.include_router(prefix_router)


def create_app():
    app_ = FastAPI(middleware=make_middleware())
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_routers(app_=app_)

    return app_


app = create_app()
