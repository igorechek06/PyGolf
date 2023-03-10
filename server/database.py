from datetime import datetime

from settings import settings
from sqlalchemy import JSON, ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

engine = create_engine(settings.database)
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
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    name: Mapped[str]
    course: Mapped[dict] = mapped_column(JSON)

    owner: Mapped[User] = relationship(User)


class Score(Base):
    __tablename__ = "scores"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    level_id: Mapped[int] = mapped_column(ForeignKey(Level.id, ondelete="CASCADE"))
    score: Mapped[int]
    date: Mapped[datetime]

    user: Mapped[User] = relationship(User)
    level: Mapped[Level] = relationship(Level)


Base.metadata.create_all(engine)
