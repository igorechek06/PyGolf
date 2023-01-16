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


class Zone(BaseModel):
    pos: Point
    size: Size

    @property
    def rect(self) -> Rect:
        return Rect(self.pos.point, self.size.size)


class FrictionZone(Zone):
    fc: float


class DeadZone(Zone):
    pass


class GolfCourse(BaseModel):
    fc: float
    size: Size

    start: Point
    finish: Point

    walls: list[Wall] = []
    zones: list[Zone] = []
