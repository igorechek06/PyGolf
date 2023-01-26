import pygame as pg
from ui import Button, Font, GameLoop, Layout

pg.init()

screen = pg.display.set_mode((750, 750), pg.RESIZABLE)
layout = Layout(screen.get_rect())
play = Button(0, 0, "Play")
editor = Button(0, 0, "Editor")
close = Button(0, 0, "Close game")
layout.add(play, editor, close)


@play.add_handler
def play_handler() -> None:
    print("Play")


@editor.add_handler
def editor_handler() -> None:
    print("Editor")


@close.add_handler
def close_handler() -> None:
    exit()


def loop(screen: pg.surface.Surface) -> None:
    screen.fill("black")
    layout.rect = screen.get_rect()
    layout.show(screen)
    pg.display.update()


main_loop = GameLoop(loop)
layout.connect_game_loop(main_loop)
main_loop.start(screen)
