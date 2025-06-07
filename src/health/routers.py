from fastapi import APIRouter, status
from src.logger import get_logger

health_router = APIRouter(prefix="/health", tags=["Health"])

logger = get_logger(__name__)


@health_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def health():
    logger.info("Health check successful")
    return {"status": "ok"}
