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
                color=models.Color(r=50, g=50, b=50),
                polygon=[
                    models.Point(x=200, y=50),
                    models.Point(x=250, y=50),
                    models.Point(x=250, y=450),
                    models.Point(x=200, y=450),
                ],
            )
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
