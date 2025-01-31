from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def SQLALCHEMY_DATABASE_URL(self):
        return self.DATABASE_URL

    class Config:
        env_file = ".env"


settings = Settings()
