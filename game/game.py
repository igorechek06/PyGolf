from tkinter import filedialog

import pygame as pg
from engine import Ball, Engine, course
from pygame.math import Vector2


def run(window: pg.surface.Surface) -> None:
    f = filedialog.askopenfilename(filetypes=[("PyGolf Level", "*.pygolf")])
    if f is None:
        return

    engine = Engine(fps=120, course=course.GolfCourse.parse_file(f))

    ball = Ball(*engine.course.start.point, 10, 10)
    engine.balls.append(ball)

    trace = False
    work = True

    @engine.set_finish_handler
    def end_game(ball: Ball) -> None:
        nonlocal work
        work = False

    while work:
        window.fill("gray")

        surface = engine.render()
        sx = (window.get_width() - surface.get_width()) // 2
        sy = (window.get_height() - surface.get_height()) // 2

        for e in pg.event.get():
            if e.type == pg.QUIT:
                work = False
            if e.type == pg.MOUSEBUTTONDOWN and ball.velocity.length() == 0:
                trace = True
            if e.type == pg.MOUSEBUTTONUP and trace:
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
