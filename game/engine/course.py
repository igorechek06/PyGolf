from enum import IntEnum, auto
from typing import Literal

from pydantic import BaseModel
from pygame import Rect


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


class Wall(BaseModel):
    start: Point
    end: Point


class ZoneType(IntEnum):
    FRICTION = auto()
    DEAD = auto()


class Zone(BaseModel):
    zone_type: ZoneType
    pos: Point
    size: Size

    @property
    def rect(self) -> Rect:
        return Rect(self.pos.point, self.size.size)


class FrictionZone(Zone):
    zone_type: Literal[ZoneType.FRICTION] = ZoneType.FRICTION
    fc: float


class DeadZone(Zone):
    zone_type: Literal[ZoneType.DEAD] = ZoneType.DEAD


class GolfCourse(BaseModel):
    fc: float
    size: Size

    start: Point
    finish: Point

    walls: list[Wall] = []
    zones: list[FrictionZone | DeadZone] = []
