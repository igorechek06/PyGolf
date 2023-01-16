from random import randint

import pygame as pg
from engine import Ball, Engine, course
from pygame.math import Vector2

engine = Engine(
    fps=75,
    course=course.GolfCourse(
        fc=0.2,
        size=course.Size(width=500, height=500),
        start=course.Point(x=250, y=450),
        finish=course.Point(x=250, y=50),
        walls=[
            course.Wall(
                start=course.Point(x=225, y=25),
                end=course.Point(x=275, y=25),
            ),
            course.Wall(
                start=course.Point(x=225, y=25),
                end=course.Point(x=225, y=75),
            ),
            course.Wall(
                start=course.Point(x=225, y=75),
                end=course.Point(x=350, y=75),
            ),
            course.Wall(
                start=course.Point(x=350, y=75),
                end=course.Point(x=450, y=175),
            ),
        ],
        zones=[
            course.FrictionZone(
                pos=course.Point(x=0, y=225),
                size=course.Size(width=500, height=25),
                fc=2,
            ),
            course.DeadZone(
                pos=course.Point(x=0, y=0),
                size=course.Size(width=500, height=10),
            ),
        ],
    ),
)

window = pg.display.set_mode((750, 750), pg.RESIZABLE)

ball = Ball(250, 450, 10, 10)
engine.balls.append(ball)

trace = False

while True:
    window.fill("gray")

    surface = engine.render()
    sx = (window.get_width() - surface.get_width()) // 2
    sy = (window.get_height() - surface.get_height()) // 2

    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
        if e.type == pg.MOUSEBUTTONDOWN:
            trace = True
        if e.type == pg.MOUSEBUTTONUP:
            mx, my = pg.mouse.get_pos()
            mx, my = mx - sx, my - sy
            ball.velocity += Vector2(mx - ball.pos.x, my - ball.pos.y) * 2
            trace = False

    if trace:
        mx, my = pg.mouse.get_pos()
        pg.draw.line(surface, "blue", ball.pos, (mx - sx, my - sy))

    window.blit(surface, (sx, sy))

    pg.display.flip()
    engine.tick()
