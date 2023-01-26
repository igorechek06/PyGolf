from abc import ABC, abstractmethod
from typing import Any

import pygame as pg


class Sprite(pg.sprite.Sprite, ABC):
    image: pg.surface.Surface
    rect: pg.rect.Rect

    def __init__(self, image: pg.surface.Surface, rect: pg.rect.Rect) -> None:
        super().__init__()
        self.image = image.copy()
        self.rect = rect.copy()

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError
