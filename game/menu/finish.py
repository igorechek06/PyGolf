import pygame as pg
from screen import screen
from ui import RELATIVE, Button, GameLoop, Layout

layout = Layout(pg.rect.Rect(0, 0, 400, 300))

back = Button(RELATIVE, "You Win!")

layout.add_widgets(back)


@GameLoop
def finish_loop() -> None:
    screen.fill("black")
    layout.rect.center = screen.get_rect().center
    layout.update()
    screen.blit(layout.image, layout.rect)
    pg.display.update()


@back.on_click
def back_clicked() -> None:
    pg.event.post(GameLoop.EXIT_EVENT)


layout.register(finish_loop)
