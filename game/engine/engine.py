from functools import wraps
from typing import Callable

import pygame as pg
from pygame.math import Vector2

from .ball import Ball
from .course import DeadZone, FrictionZone, GolfCourse


class Engine:
    fps: int
    course: GolfCourse

    balls: list[Ball]
    clock: pg.time.Clock

    finish_handlers: list[Callable[[Ball], None]]

    def __init__(self, fps: int, course: GolfCourse) -> None:
        self.fps = fps
        self.course = course

        self.balls = []
        self.clock = pg.time.Clock()

        self.finish_handlers = []

    def set_finish_handler(
        self, func: Callable[[Ball], None]
    ) -> Callable[[Ball], None]:
        self.finish_handlers.append(func)
        return func

    # Render
    def render(self) -> pg.surface.Surface:
        surface = pg.surface.Surface(self.course.size.size)

        for zone in self.course.zones:
            if isinstance(zone, FrictionZone):
                color = "yellow"
            elif isinstance(zone, DeadZone):
                color = "red"
            else:
                print(zone, type(zone))
            pg.draw.rect(surface, color, zone.rect)

        for wall in self.course.walls:
            pg.draw.line(surface, "gray", wall.start.point, wall.end.point, 5)

        pg.draw.circle(surface, "green", self.course.finish.point, 10)

        for ball in self.balls:
            pg.draw.circle(surface, "white", ball.pos, ball.radius)

        return surface

    # Calc
    def tick(self) -> None:
        t = self.clock.tick(self.fps) / 1000

        for ball in self.balls:
            fc = self.course.fc
            for zone in self.course.zones:
                if zone.rect.colliderect(ball.rect):
                    if isinstance(zone, FrictionZone):
                        fc = zone.fc
                    elif isinstance(zone, DeadZone):
                        ball.velocity = Vector2()
                        ball.pos = Vector2(self.course.start.point)

            if ball.velocity.length() != 0:
                if (
                    ball.pos.x + ball.radius >= self.course.size.width
                    and ball.velocity.x > 0
                    or ball.pos.x - ball.radius <= 0
                    and ball.velocity.x < 0
                ):
                    ball.velocity.reflect_ip(Vector2(1, 0))
                if (
                    ball.pos.y + ball.radius >= self.course.size.height
                    and ball.velocity.y > 0
                    or ball.pos.y - ball.radius <= 0
                    and ball.velocity.y < 0
                ):
                    ball.velocity.reflect_ip(Vector2(0, 1))

                for wall in self.course.walls:
                    if ball.collide_line((wall.start.point, wall.end.point)):
                        ball.velocity.reflect_ip(
                            Vector2(
                                wall.end.y - wall.start.y, -(wall.end.x - wall.start.x)
                            )
                        )

                a = -ball.velocity.normalize() * fc * 9.8
                ball.pos += ball.velocity * t + (a * t**2) / 2
                ball.velocity += a

                if ball.velocity.length() - a.length() <= 0:
                    ball.velocity = Vector2()

            if (
                ball.rect.collidepoint(self.course.finish.point)
                and ball.velocity.length() <= 500
            ):
                for handler in self.finish_handlers:
                    handler(ball)

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
