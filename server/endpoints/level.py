import database as db
import models as m
from dependencies import auth
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel


class Level(BaseModel):
    name: str
    course: m.Course


router = APIRouter(prefix="/level")


@router.post("/")
def push_level(level: Level, user: db.User = Depends(auth)) -> None:
    with db.session.begin() as session:
        session.add(
            db.Level(
                name=level.name,
                course=level.course.dict(),
                owner_id=user.id,
            ),
        )


@router.get("/find")
def find_levels(
    name: str | None = None,
    limit: int = 10,
    offset: int = 0,
) -> list[m.Level]:
    if limit > 10:
        raise HTTPException(400, "limit должен быть <=10")
    with db.session() as session:
        query = session.query(db.Level)
        if name is not None:
            query = query.filter(db.Level.name.like(f"%{name}%"))
        query = query.order_by(db.Level.id.desc()).offset(offset).limit(limit)

        return [m.Level.from_orm(o) for o in query.all()]


@router.get("/{id}")
def get_by_id(id: int) -> m.Level | None:
    with db.session() as session:
        level = session.get(db.Level, id)
        if level is None:
            return None
        return m.Level.from_orm(level)
