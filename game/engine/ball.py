from math import sqrt

import pygame as pg
from pygame.math import Vector2


class Ball:
    x: float
    y: float
    radius: float
    mass: float
    velocity: Vector2

    def __init__(
        self,
        x: float,
        y: float,
        radius: float,
        mass: float,
        velocity: Vector2 | None = None,
    ) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.velocity = Vector2() if velocity is None else velocity

    @property
    def pos(self) -> tuple[float, float]:
        return (self.x, self.y)

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )

    def collide_ball(self, ball: "Ball") -> bool:
        return (
            sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
            <= self.radius + ball.radius
        )
