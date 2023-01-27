from abc import ABC, abstractmethod

import pygame as pg
from sprite import Sprite

from . import GameLoop

RELATIVE = pg.rect.Rect(0, 0, 0, 0)


class Widget(Sprite, ABC):
    def __init__(self, rect: pg.rect.Rect) -> None:
        super().__init__(pg.surface.Surface(rect.size), rect)

    @property
    def rel_rect(self) -> pg.rect.Rect:
        return pg.rect.Rect((0, 0), self.rect.size)

    @rel_rect.setter
    def rel_rect(self, value: pg.rect.Rect) -> None:
        self.rect.x += value.x
        self.rect.y += value.y

    @abstractmethod
    def register(self, loop: GameLoop) -> GameLoop:
        raise NotImplementedError
