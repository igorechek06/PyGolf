import pydantic


class Settings(pydantic.BaseSettings):
    database: str
    secret: str


settings = Settings()
