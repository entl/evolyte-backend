from typing import List

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.responses import JSONResponse

from src.core.middlewares.auth_middleware import AuthenticationMiddleware, AuthBackend
from src.core.exceptions.base import CustomException
from src.health.routers import health_router
from src.user.routers import users_router
from src.auth.routers import auth_router
from src.solar_panels.routers import solar_panels_router
from src.pvgis.routers import pvgis_router
from src.predict.routers import predict_router
from src.weather.routers import weather_router

from src.settings import settings

# index models
from src.solar_panels.models import SolarPanel
from src.user.models import User

# disable warning
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


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
            allow_origins=settings.cors_origins,
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


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def init_routers(app_: FastAPI) -> None:
    prefix_router = APIRouter(prefix="/api/v1")
    prefix_router.include_router(health_router)
    prefix_router.include_router(users_router)
    prefix_router.include_router(auth_router)
    prefix_router.include_router(solar_panels_router)
    prefix_router.include_router(pvgis_router)
    prefix_router.include_router(predict_router)
    prefix_router.include_router(weather_router)

    app_.include_router(prefix_router)


def create_app():
    app_ = FastAPI(middleware=make_middleware())

    init_listeners(app_=app_)
    init_routers(app_=app_)

    return app_


app = create_app()
