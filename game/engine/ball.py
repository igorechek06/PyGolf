from math import sqrt

import pygame as pg
from pygame.math import Vector2


class Ball:
    pos: Vector2
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
        self.pos = Vector2(x, y)
        self.radius = radius
        self.mass = mass
        self.velocity = Vector2() if velocity is None else velocity

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(
            self.pos.x - self.radius,
            self.pos.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def collide_ball(self, ball: "Ball") -> bool:
        return (
            ball is not self
            and Vector2(self.pos - ball.pos).length() <= self.radius + ball.radius
        )

    def collide_line(
        self,
        line: tuple[tuple[int, int], tuple[int, int]],
    ) -> bool:
        return (
            min(line[0][0], line[1][0]) <= self.pos.x <= max(line[0][0], line[1][0])
            or min(line[0][1], line[1][1]) <= self.pos.y <= max(line[0][1], line[1][1])
        ) and abs(
            (line[1][0] - line[0][0]) * (line[0][1] - self.pos.y)
            - (line[0][0] - self.pos.x) * (line[1][1] - line[0][1])
        ) / sqrt(
            (line[1][0] - line[0][0]) ** 2 + (line[1][1] - line[0][1]) ** 2
        ) <= self.radius
