from math import sqrt

import pygame as pg
from pygame.math import Vector2

from .ball import Ball


class Engine:
    fps: int
    fc: float  # Friction coefficient
    window: pg.surface.Surface
    clock: pg.time.Clock
    balls: list[Ball]

    def __init__(
        self,
        fps: int,
        fc: float,
        window: pg.surface.Surface,
        balls: list[Ball],
    ) -> None:
        self.fps = fps
        self.fc = fc
        self.window = window
        self.clock = pg.time.Clock()
        self.balls = balls

    def draw(self) -> None:
        for ball in self.balls:
            pg.draw.circle(self.window, (255, 255, 255), (ball.x, ball.y), 5)

    def get_collidepoint_ball(self, point: tuple[float, float]) -> Ball | None:
        for ball in self.balls:
            if pg.Rect(ball.x - 5, ball.y - 5, 10, 10).collidepoint(point):
                return ball
        return None

    def tick(self) -> None:
        t = self.clock.tick(self.fps) / 1000

        for ball in self.balls:
            if ball.velocity.length() != 0:
                a = -ball.velocity.normalize() * self.fc * 9.8

                if ball.x + 5 >= self.window.get_width() or ball.x - 5 <= 0:
                    ball.velocity.reflect_ip(Vector2(1, 0))
                if ball.y + 5 >= self.window.get_height() or ball.y - 5 <= 0:
                    ball.velocity.reflect_ip(Vector2(0, 1))

                ball.x += ball.velocity.x * t + (a.x * t**2) / 2
                ball.y += ball.velocity.y * t + (a.y * t**2) / 2
                ball.velocity += a

                if ball.velocity.length() - a.length() <= 0:
                    ball.velocity = Vector2()
