import keyring
import models
import pygame as pg
from engine import Course
from menu import account_loop, game_loop
from screen import screen
from ui import RELATIVE, Button, GameLoop, Layout

main_layout = Layout(pg.rect.Rect(0, 0, 400, 300))

account = Button(RELATIVE, "Account")
play = Button(RELATIVE, "Play")
editor = Button(RELATIVE, "Editor")
close = Button(RELATIVE, "Close")

main_layout.add_widgets(account, play, editor, close)


@GameLoop
def main_loop() -> None:
    screen.fill("black")
    main_layout.rect.center = screen.get_rect().center
    main_layout.update()
    screen.blit(main_layout.image, main_layout.rect)
    pg.display.update()


@account.on_click
def account_clicked() -> None:
    account_loop.start(keyring.get_password("pygolf", "token"))


@play.on_click
def play_clicked() -> None:
    game_loop.start(Course(60, models.Course.parse_file("map.pygolf")))


@editor.on_click
def editor_clicked() -> None:
    import editor

    editor.editor_loop.start()


@close.on_click
def close_clicked() -> None:
    pg.event.post(GameLoop.EXIT_EVENT)


main_layout.register(main_loop)
main_loop.start()
