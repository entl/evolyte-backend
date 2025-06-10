# disable warning
import warnings
from contextlib import asynccontextmanager
from typing import List

import redis
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.responses import JSONResponse

from src.auth.routers import auth_router
from src.auth.google.routers import google_auth_router
from src.core.exceptions.base import CustomException
from src.core.middlewares.auth_middleware import AuthBackend, AuthenticationMiddleware
from src.core.middlewares.rate_limiter_middleware import RateLimiterMiddleware
from src.health.routers import health_router
from src.predict.routers import predict_router
from src.pvgis.routers import pvgis_router
from src.user.routers import users_router
from src.weather.routers import weather_router
from src.solar_panels.routers import solar_panels_router
from src.settings import settings
from src.logger import setup_logging, get_logger

# index models
from src.solar_panels.models import SolarPanel  # noqa
from src.user.models import User  # noqa
from src.auth.models import Identity  # noqa

logger = get_logger(__name__)

warnings.simplefilter(action="ignore", category=FutureWarning)


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


def add_middlewares(app_: FastAPI) -> None:
    logger.debug("Adding middlewares to the FastAPI application")
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app_.add_middleware(
        RateLimiterMiddleware,
        redis_client=app_.state.redis,
    )
    app_.add_middleware(
        AuthenticationMiddleware,
        backend=AuthBackend(),
        on_error=on_auth_error,
    )
    logger.debug("Middlewares added successfully")


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def init_redis(app_: FastAPI) -> None:
    pool = redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port, db=settings.redis_cache_db)
    app_.state.redis = redis.Redis.from_pool(pool)

    if app_.state.redis.ping():
        logger.debug("Redis connection established successfully.")
    else:
        logger.error("Failed to connect to Redis.")
        raise Exception("Failed to connect to Redis.")


def init_routers(app_: FastAPI) -> None:
    logger.debug("Initializing routers for the FastAPI application")
    prefix_router = APIRouter(prefix="/api/v1")
    prefix_router.include_router(health_router)
    prefix_router.include_router(users_router)
    prefix_router.include_router(auth_router)
    prefix_router.include_router(google_auth_router)
    prefix_router.include_router(solar_panels_router)
    prefix_router.include_router(pvgis_router)
    prefix_router.include_router(predict_router)
    prefix_router.include_router(weather_router)

    app_.include_router(prefix_router)
    logger.debug("Routers initialized successfully")


@asynccontextmanager
async def lifespan(app_: FastAPI):
    init_redis(app_)
    logger.debug("Application startup: Initializing Redis connection")
    yield
    logger.debug("Application shutdown: Closing Redis connection")
    await app_.state.redis.close()


def create_app():
    app_ = FastAPI()
    setup_logging()
    logger.error("test error log")
    init_redis(app_)

    add_middlewares(app_=app_)

    init_listeners(app_=app_)
    init_routers(app_=app_)

    return app_


app = create_app()
