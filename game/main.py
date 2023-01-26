import pygame as pg
from sprite import Sprite
from ui import Button, Field, GameLoop, Layout

pg.init()

screen = pg.display.set_mode((750, 750), pg.RESIZABLE)

layout = Layout(pg.rect.Rect(0, 0, 400, 300))

play = Button(pg.rect.Rect(0, 0, 200, 100), "Play")
editor = Button(pg.rect.Rect(0, 0, 200, 100), "Editor")
close = Button(pg.rect.Rect(0, 0, 200, 100), "Close")

layout.add_widgets(play, editor, close)


@GameLoop
def loop(screen: pg.surface.Surface, layout: Layout) -> None:
    screen.fill("black")
    layout.rect.center = screen.get_rect().center
    layout.update()
    screen.blit(layout.image, layout.rect)
    pg.display.update()


@play.on_click()
def play_clicked() -> None:
    print("Play")


@editor.on_click()
def editor_clicked() -> None:
    print("Editor")


@close.on_click()
def close_clicked() -> None:
    exit()


layout.register(loop)
loop.start(screen, layout)
