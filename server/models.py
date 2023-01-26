from datetime import datetime
from enum import IntEnum, auto

from pydantic import BaseModel


class OrmModel(BaseModel):
    class Config:
        orm_mode = True


class Point(BaseModel):
    x: int
    y: int

    @property
    def point(self) -> tuple[int, int]:
        return (self.x, self.y)


class Size(BaseModel):
    width: int
    height: int

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)


class Color(BaseModel):
    r: int
    g: int
    b: int

    @property
    def color(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)


class Wall(BaseModel):
    start: Point
    end: Point
    color: Color
    width: int = 5


class ZoneType(IntEnum):
    FRICTION = auto()
    DEAD = auto()


class Zone(BaseModel):
    zone_type: ZoneType
    pos: Point
    size: Size


class FrictionZone(Zone):
    zone_type = ZoneType.FRICTION
    friction: float


class DeadZone(Zone):
    zone_type = ZoneType.DEAD


class Course(BaseModel):
    friction: float
    size: Size

    start: Point
    finish: Point

    walls: list[Wall] = []
    zone: list[FrictionZone | DeadZone] = []


class User(OrmModel):
    id: int
    username: str


class Level(OrmModel):
    id: int
    owner: User
    name: str
    course: Course


class Score(OrmModel):
    user: User
    level: Level
    score: int
    date: datetime
