from random import randint

import pygame as pg
from engine import Ball, Engine
from pygame.math import Vector2

engine = Engine(
    fps=75,
    fc=0.4,
    window=pg.display.set_mode((1000, 1000), pg.RESIZABLE),
    balls=[Ball(randint(20, 980), randint(20, 980), 20, 10) for _ in range(10)],
)

x, y = 0.0, 0.0
ball = None


def get_collidepoint_ball(point: tuple[float, float]) -> Ball | None:
    for ball in engine.balls:
        if ball.rect.collidepoint(point):
            return ball
    return None


while True:
    engine.window.fill("black")

    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
        elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            ball = get_collidepoint_ball(e.pos)
            if ball is not None:
                x, y = ball.pos
        elif e.type == pg.MOUSEMOTION and ball is not None:
            x, y = e.pos
        elif e.type == pg.MOUSEBUTTONUP and e.button == 1:
            if ball is not None:
                ball.velocity += Vector2(x - ball.x, y - ball.y).normalize() * 1000
                ball = None

    if ball is not None:
        pg.draw.line(engine.window, "red", ball.pos, (x, y))

    for b in engine.balls:
        pg.draw.circle(engine.window, "white", (b.x, b.y), b.radius)

    pg.display.flip()
    engine.tick()
