import models
import pygame as pg
from engine import Ball, Course

screen = pg.display.set_mode((750, 750), pg.RESIZABLE)

course = Course(
    60,
    models.Course(
        friction=0.2,
        size=models.Size(width=500, height=500),
        start=models.Point(x=100, y=100),
        finish=models.Point(x=400, y=400),
        walls=[
            models.Wall(
                color=models.Color(r=100, g=100, b=100),
                polygon=[
                    models.Point(x=206, y=336),
                    models.Point(x=295, y=333),
                    models.Point(x=307, y=245),
                ],
            ),
            models.Wall(
                color=models.Color(r=100, g=100, b=100),
                polygon=[
                    models.Point(x=208, y=388),
                    models.Point(x=292, y=384),
                    models.Point(x=291, y=497),
                    models.Point(x=218, y=493),
                    models.Point(x=215, y=461),
                    models.Point(x=266, y=461),
                    models.Point(x=265, y=414),
                    models.Point(x=212, y=412),
                ],
            ),
            models.Wall(
                color=models.Color(r=100, g=100, b=100),
                polygon=[
                    models.Point(x=202, y=66),
                    models.Point(x=190, y=172),
                    models.Point(x=362, y=68),
                    models.Point(x=353, y=164),
                ],
            ),
        ],
        zone=[
            models.DeadZone(
                pos=models.Point(x=425, y=0),
                size=models.Size(width=75, height=75),
            ),
            models.FrictionZone(
                friction=2,
                pos=models.Point(x=300, y=300),
                size=models.Size(width=100, height=100),
            ),
        ],
    ),
)
ball: Ball = course.add_ball()

while True:
    screen.fill("gray")

    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                ball.velocity += (
                    pg.math.Vector2(
                        e.pos[0] - ball.pos.x - 125, e.pos[1] - ball.pos.y - 125
                    )
                    * 2
                )

            if e.button == 3:
                ball = course.add_ball()

    game = course.render()
    screen.blit(game, (125, 125))

    course.update()
    pg.display.update()
