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
    game_loop.start(
        Course(
            60,
            models.Course(
                friction=0.2,
                size=models.Size(width=500, height=500),
                start=models.Point(x=100, y=100),
                finish=models.Point(x=400, y=400),
                walls=[
                    models.Wall(
                        start=models.Point(x=250, y=100),
                        end=models.Point(x=200, y=400),
                        color=models.Color(r=75, g=75, b=75),
                        width=100,
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
    )


@editor.on_click
def editor_clicked() -> None:
    print("Editor")


@close.on_click
def close_clicked() -> None:
    pg.event.post(GameLoop.EXIT_EVENT)


main_layout.register(main_loop)
main_loop.start()
