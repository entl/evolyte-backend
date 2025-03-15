from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_database_hostname: str
    pg_database_port: str
    pg_database_password: str
    pg_database_name: str
    pg_database_username: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_token_expire_minutes: int

    ml_api_url: str

    class Config:
        env_file = ".env"


settings = Settings()
