from random import randint

import pygame as pg
import src
from pygame.math import Vector2

from . import Sprite


class Ball(Sprite):
    pos: Vector2
    radius: int
    mass: float
    velocity: Vector2

    def __init__(
        self,
        pos: tuple[int, int],
        radius: int,
        mass: float,
        velocity: Vector2 | None = None,
    ) -> None:
        self.pos = Vector2(pos)
        self.radius = radius
        self.mass = mass
        self.velocity = Vector2() if velocity is None else velocity

        image = pg.surface.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        pg.draw.circle(
            image,
            (randint(0, 255), randint(0, 255), randint(0, 255)),
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

    def update(self, time: float, friction: float) -> None:
        if self.velocity.length() != 0:

            acceleration = -self.velocity.normalize() * friction * 9.8
            self.pos += self.velocity * time + (acceleration * time**2) / 2
            self.velocity += acceleration

            if self.velocity.length() - acceleration.length() <= 0:
                self.velocity = Vector2()

            self.rect = self.get_rect()
