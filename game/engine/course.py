import models
import pygame as pg
import src

from . import Ball, DeadZone, FrictionZone, Sprite, Wall, Zone


def zone(zone: models.Zone) -> Zone:
    if isinstance(zone, models.FrictionZone):
        return FrictionZone(zone.friction, zone.pos.point, zone.size.size)
    elif isinstance(zone, models.DeadZone):
        return DeadZone(zone.pos.point, zone.size.size)


class Finish(Sprite):
    pos: tuple[int, int]

    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(
            src.image.finish, pg.rect.Rect(pos, src.image.finish.get_size())
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
        self.walls = [Wall(w.color.color, w.wall) for w in model.walls]
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
        ball = Ball(self.model.start.point, 10, 5)
        self.balls.append(ball)
        return ball

    def update(self) -> None:
        time = self.clock.tick(self.fps) / 1000

        for ball in self.balls:
            friction = self.model.friction
            for zone in self.zones:
                if not pg.sprite.collide_mask(zone, ball):
                    continue
                if isinstance(zone, FrictionZone):
                    friction = zone.friction
                if isinstance(zone, DeadZone):
                    ball.velocity = pg.math.Vector2()
                    ball.pos = pg.math.Vector2(self.model.start.point)
                    ball.rect = ball.get_rect()

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

            if (
                ball.pos.x + ball.radius >= self.model.size.width
                and ball.velocity.x > 0
                or ball.pos.x - ball.radius <= 0
                and ball.velocity.x < 0
            ):
                ball.velocity.reflect_ip(pg.math.Vector2(1, 0))
            if (
                ball.pos.y + ball.radius >= self.model.size.height
                and ball.velocity.y > 0
                or ball.pos.y - ball.radius <= 0
                and ball.velocity.y < 0
            ):
                ball.velocity.reflect_ip(pg.math.Vector2(0, 1))

            # for wall in self.walls:
            #     collide = pg.sprite.collide_mask(wall, ball)
            #     if collide is None:
            #         continue

            ball.update(time, friction)