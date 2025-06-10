from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from redis import Redis
from src.redis_repository import RedisBaseRepository


class RateLimiterMiddleware(BaseHTTPMiddleware):
    # TODO: Assess benefits of decorator rate limiting
    def __init__(self, app, redis_client: Redis):
        super().__init__(app)
        self.rate_limit = 100  # Example limit: 100 requests per minute
        self.time_window = 60
        self.namespace = "rate_limiter_middleware"
        self.redis_repository = RedisBaseRepository(redis_client, namespace=self.namespace)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        path = request.url.path
        format_key = f"{client_ip}:{path}"

        current_count = self.redis_repository.incr(format_key, 1)

        if current_count == 1:
            self.redis_repository.expire(format_key, self.time_window)

        if current_count > self.rate_limit:
            return Response(
                content="Rate limit exceeded. Try again later.",
                status_code=429,
            )

        response: Response = await call_next(request)
        return response
