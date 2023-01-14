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

    def tick(self) -> None:
        t = self.clock.tick(self.fps) / 1000

        for ball in self.balls:
            for collided_ball in filter(lambda b: b.collide_ball(ball), self.balls):
                b1 = ball
                b2 = collided_ball

                v1 = b1.velocity - (
                    ((2 * b2.mass) / (b1.mass + b2.mass))
                    * (
                        ((b1.velocity - b2.velocity).dot(b1.pos - b2.pos))
                        / (b1.pos - b2.pos).length_squared()
                    )
                    * (b1.pos - b2.pos)
                )
                v2 = b2.velocity - (
                    ((2 * b1.mass) / (b1.mass + b2.mass))
                    * (
                        ((b2.velocity - b1.velocity).dot(b2.pos - b1.pos))
                        / (b2.pos - b1.pos).length_squared()
                    )
                    * (b2.pos - b1.pos)
                )

                b1.velocity = v1
                b2.velocity = v2
                break

            if ball.velocity.length() != 0:
                if (
                    ball.pos.x + ball.radius >= self.window.get_width()
                    and ball.velocity.x > 0
                    or ball.pos.x - ball.radius <= 0
                    and ball.velocity.x < 0
                ):
                    ball.velocity.reflect_ip(Vector2(1, 0))
                if (
                    ball.pos.y + ball.radius >= self.window.get_height()
                    and ball.velocity.y > 0
                    or ball.pos.y - ball.radius <= 0
                    and ball.velocity.y < 0
                ):
                    ball.velocity.reflect_ip(Vector2(0, 1))

                a = -ball.velocity.normalize() * self.fc * 9.8
                ball.pos += ball.velocity * t + (a * t**2) / 2
                ball.velocity += a

                if ball.velocity.length() - a.length() <= 0:
                    ball.velocity = Vector2()
