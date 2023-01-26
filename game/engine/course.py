from random import randint

import collision
import models
import pygame as pg
import src
from pygame.math import Vector2
from sprite import Sprite

from . import Ball, DeadZone, FrictionZone, Wall, Zone


def zone(zone: models.Zone) -> Zone:
    if isinstance(zone, models.FrictionZone):
        return FrictionZone(zone.friction, zone.pos.point, zone.size.size)
    elif isinstance(zone, models.DeadZone):
        return DeadZone(zone.pos.point, zone.size.size)
    raise TypeError


class Finish(Sprite):
    pos: tuple[int, int]

    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(
            src.sprites.finish, pg.rect.Rect(pos, src.sprites.finish.get_size())
        )
        self.pos = pos


class Course:
    fps: int
    model: models.Course

    finish: Finish
    balls: list[Ball]
    walls: list[Wall]
    zones: list[Zone]
    clock: pg.time.Clock

    def __init__(self, fps: int, model: models.Course) -> None:
        self.fps = fps
        self.model = model

        self.finish = Finish(self.model.finish.point)
        self.balls = []
        self.walls = [
            Wall(w.start.point, w.end.point, w.color.color, w.width)
            for w in model.walls
        ]
        self.zones = [zone(z) for z in model.zone]
        self.clock = pg.time.Clock()

    def render(self) -> pg.surface.Surface:
        surface = pg.surface.Surface(self.model.size.size)

        surface.blit(self.finish.image, self.finish.rect)  # Finish
        surface.blits([(zone.image, zone.rect) for zone in self.zones])  # Zones
        surface.blits([(wall.image, wall.rect) for wall in self.walls])  # Walls
        surface.blits([(ball.image, ball.rect) for ball in self.balls])  # Balls

        return surface

    def add_ball(self) -> Ball:
        ball = Ball(
            self.model.start.point,
            10,
            5,
            (randint(0, 255), randint(0, 255), randint(0, 255)),
        )
        self.balls.append(ball)
        return ball

    def update_impulse(self, ball: Ball) -> None:
        for collided_ball in self.balls:
            if (
                ball is collided_ball
                or (collided_ball.pos - ball.pos).length_squared() == 0
                or not pg.sprite.collide_circle(collided_ball, ball)
            ):
                continue

            b1 = collided_ball
            b2 = ball

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

    def update_collision(self, ball: Ball) -> None:
        if (
            ball.pos.x + ball.radius >= self.model.size.width
            and ball.velocity.x > 0
            or ball.pos.x - ball.radius <= 0
            and ball.velocity.x < 0
        ):
            ball.velocity.reflect_ip(Vector2(1, 0))
        if (
            ball.pos.y + ball.radius >= self.model.size.height
            and ball.velocity.y > 0
            or ball.pos.y - ball.radius <= 0
            and ball.velocity.y < 0
        ):
            ball.velocity.reflect_ip(Vector2(0, 1))

        for wall in self.walls:
            response = collision.Response()
            wall_collider = collision.Poly(
                collision.Vector(wall.rect.x, wall.rect.y),
                [collision.Vector(p[0], p[1]) for p in wall.rel_points],
            )
            ball_collider = collision.Circle(
                collision.Vector(ball.pos.x, ball.pos.y),
                ball.radius,
            )

            if not collision.test_poly_circle(
                wall_collider,
                ball_collider,
                response,
            ):
                continue
            edge = Vector2(response.overlap_v.x, response.overlap_v.y)
            if edge.length() != 0:
                ball.velocity.reflect_ip(edge)

    def update_ball(self, ball: Ball, time: float) -> None:
        friction = self.model.friction

        for zone in self.zones:
            if pg.sprite.collide_mask(zone, ball):
                if isinstance(zone, FrictionZone):
                    friction = zone.friction
                if isinstance(zone, DeadZone):
                    ball.velocity = Vector2()
                    ball.pos = Vector2(self.model.start.point)
                    ball.update()

        if ball.velocity.length() != 0:
            acceleration = -ball.velocity.normalize() * friction * 9.8
            ball.pos += ball.velocity * time + (acceleration * time**2) / 2
            ball.velocity += acceleration

            if ball.velocity.length() - acceleration.length() <= 0:
                ball.velocity = Vector2()

            ball.update()

    def update(self) -> None:
        time = self.clock.tick(self.fps) / 1000

        for ball in self.balls:
            self.update_impulse(ball)
            self.update_collision(ball)
            self.update_ball(ball, time)
