from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_database_hostname: str
    pg_database_port: str
    pg_database_password: str
    pg_database_name: str
    pg_database_username: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_token_expiration_time: int  # in seconds
    jwt_refresh_token_expiration_time: int  # in seconds

    ml_api_url: str

    google_client_id: str
    google_client_secret: str

    cors_origins: list[str]

    env: str

    class Config:
        env_file = ".env.dev"


settings = Settings()
