import pygame as pg
from engine import Ball, Course
from screen import screen
from ui import GameLoop

ball: Ball
course: Course
rect: pg.rect.Rect


@GameLoop
def game_loop(local_course: Course) -> None:
    global rect
    screen.fill("gray")

    game = local_course.render()
    rect = game.get_rect()
    rect.center = screen.get_rect().center

    screen.blit(game, rect)

    local_course.update()
    pg.display.update()


@game_loop.set_setup
def setup(local_course: Course) -> None:
    global ball, button, course

    @local_course.on_finish
    def finish(winner: Ball) -> None:
        global ball
        from menu import finish_loop

        course.balls.remove(winner)

        if len(course.balls) <= 0:
            finish_loop.start()
            pg.event.post(GameLoop.EXIT_EVENT)
        else:
            ball = course.balls[-1]

    course = local_course
    ball = course.add_ball()


@game_loop.event_handler(pg.KEYDOWN)
def key_event(event: pg.event.Event) -> None:
    if event.key == pg.K_ESCAPE:
        pg.event.post(GameLoop.EXIT_EVENT)


@game_loop.event_handler(pg.MOUSEBUTTONDOWN)
def mouse_event(event: pg.event.Event) -> None:
    global ball, course
    if event.button == 1 and ball.velocity.length() == 0:
        ball.velocity = (
            pg.math.Vector2(
                event.pos[0] - rect.x - ball.pos.x, event.pos[1] - rect.y - ball.pos.y
            ).normalize()
            * 500
        )
    if event.button == 3:
        ball = course.add_ball()
