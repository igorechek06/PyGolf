import pygame as pg


class Sprite(pg.sprite.Sprite):
    image: pg.surface.Surface
    rect: pg.rect.Rect

    def __init__(self, image: pg.surface.Surface, rect: pg.rect.Rect) -> None:
        super().__init__()
        self.image = image.copy()
        self.rect = rect.copy()
