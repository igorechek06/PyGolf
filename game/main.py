from random import randint as r

import pygame as pg
from engine import Ball, Engine
from pygame.math import Vector2

engine = Engine(
    fps=60,
    fc=1,
    window=pg.display.set_mode((500, 500), pg.RESIZABLE),
    balls=[Ball(r(5, 495), r(4, 495)) for _ in range(10)],
)

x, y = 0.0, 0.0
ball = None

while True:
    engine.window.fill("black")

    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
        elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            ball = engine.get_collidepoint_ball(e.pos)
            if ball is not None:
                x, y = ball.pos
        elif e.type == pg.MOUSEMOTION and ball is not None:
            x, y = e.pos
        elif e.type == pg.MOUSEBUTTONUP and e.button == 1:
            if ball is not None:
                ball.velocity += Vector2(x - ball.x, y - ball.y) * 5
                ball = None

    if ball is not None:
        pg.draw.line(engine.window, (255, 0, 0), ball.pos, (x, y))

    engine.draw()

    pg.display.flip()
    engine.tick()

