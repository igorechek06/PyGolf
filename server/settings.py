import pydantic


class Settings(pydantic.BaseSettings):
    database_url: str
    secret: str


settings = Settings()
