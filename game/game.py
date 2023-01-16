import pygame as pg
from engine import Ball, Engine, course
from pygame.math import Vector2
from tkinter import filedialog


def run(window: pg.surface.Surface) -> None:
    engine = Engine(
        fps=60,
        course=course.GolfCourse.parse_file(filedialog.askopenfilename()),
    )

    ball = Ball(*engine.course.start.point, 10, 10)
    engine.balls.append(ball)

    trace = False

    while True:
        window.fill("gray")

        surface = engine.render()
        sx = (window.get_width() - surface.get_width()) // 2
        sy = (window.get_height() - surface.get_height()) // 2

        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
            if e.type == pg.MOUSEBUTTONDOWN:
                trace = True
            if e.type == pg.MOUSEBUTTONUP:
                mx, my = pg.mouse.get_pos()
                mx, my = mx - sx, my - sy
                ball.velocity = Vector2(mx - ball.pos.x, my - ball.pos.y) * 2
                trace = False

        if trace:
            mx, my = pg.mouse.get_pos()
            pg.draw.line(surface, "blue", ball.pos, (mx - sx, my - sy))

        window.blit(surface, (sx, sy))

        pg.display.flip()
        engine.tick()
