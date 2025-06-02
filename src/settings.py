from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_database_hostname: str
    pg_database_port: str
    pg_database_password: str
    pg_database_name: str
    pg_database_username: str

    redis_host: str
    redis_port: str
    redis_password: str
    redis_cache_db: str
    redis_celery_broker_db: str
    redis_celery_backend_db: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_token_expiration_time: int  # in seconds
    jwt_refresh_token_expiration_time: int  # in seconds

    ml_api_url: str

    google_client_id: str
    google_client_secret: str

    enode_client_id: str
    enode_client_secret: str
    enode_api_url: str
    enode_oauth_url: str

    cors_origins: list[str]

    env: str

    class Config:
        env_file = ".env.dev"


settings = Settings()
