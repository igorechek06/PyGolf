from settings import settings
from sqlalchemy import JSON, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine(settings.database_url)
session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    salt: Mapped[str]


class Level(Base):
    __tablename__ = "levels"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    course: Mapped[dict] = mapped_column(JSON)
