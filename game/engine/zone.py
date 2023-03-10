import pygame as pg
import src
from sprite import Sprite


class Zone(Sprite):
    pos: tuple[int, int]
    size: tuple[int, int]

    def __init__(
        self,
        pos: tuple[int, int],
        size: tuple[int, int],
        image: pg.surface.Surface,
    ) -> None:
        super().__init__(pg.transform.scale(image, size), pg.rect.Rect(pos, size))
        self.pos = pos
        self.size = size

    def update(self) -> None:
        pass


class FrictionZone(Zone):
    friction: float

    def __init__(
        self,
        friction: float,
        pos: tuple[int, int],
        size: tuple[int, int],
    ) -> None:
        super().__init__(pos, size, src.sprites.zone.friction)
        self.friction = friction


class DeadZone(Zone):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]) -> None:
        super().__init__(pos, size, src.sprites.zone.dead)
