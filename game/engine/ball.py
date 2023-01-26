import pygame as pg
import src
from pygame.math import Vector2

from . import Sprite


class Ball(Sprite):
    pos: Vector2
    radius: int
    mass: float
    color: tuple[int, int, int]
    velocity: Vector2

    def __init__(
        self,
        pos: tuple[int, int],
        radius: int,
        mass: float,
        color: tuple[int, int, int],
        velocity: Vector2 | None = None,
    ) -> None:
        self.pos = Vector2(pos)
        self.radius = radius
        self.mass = mass
        self.color = color
        self.velocity = Vector2() if velocity is None else velocity

        image = pg.surface.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        pg.draw.circle(
            image,
            color,
            (self.radius, self.radius),
            self.radius - 1,
        )
        image.blit(
            pg.transform.scale(src.image.ball, image.get_size()),
            (0, 0),
        )
        super().__init__(image, self.get_rect())

    def get_rect(self) -> pg.rect.Rect:
        return pg.rect.Rect(
            self.pos - Vector2(self.radius), (self.radius * 2, self.radius * 2)
        )

    def update(self) -> None:
        self.rect = self.get_rect()
