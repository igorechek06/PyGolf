import pygame as pg
from screen import screen
from ui import RELATIVE, Button, Field, GameLoop, Layout

layout = Layout(pg.rect.Rect(0, 0, 400, 300))

username = Field(RELATIVE, "Username")
password = Field(RELATIVE, "Password", hide=True)
back = Button(RELATIVE, "Back")

action_layout = Layout(RELATIVE, Layout.Mode.VERTICAL)

login = Button(RELATIVE, "Login")
register = Button(RELATIVE, "Register")

save = Button(RELATIVE, "Save")
delete = Button(RELATIVE, "Delete")

layout.add_widgets(username, password, action_layout, back)


@GameLoop
def account_loop(token: str | None) -> None:
    screen.fill("black")
    layout.rect.center = screen.get_rect().center
    layout.update()
    screen.blit(layout.image, layout.rect)
    pg.display.update()


@account_loop.set_setup
def loop_setup(token: str | None) -> None:
    action_layout.widgets.clear()
    if token is None:
        action_layout.add_widgets(login, register)
    else:
        action_layout.add_widgets(save, delete)
    action_layout.register(account_loop)


@back.on_click
def back_clicked() -> None:
    pg.event.post(GameLoop.EXIT_EVENT)


@login.on_click
def login_clicked() -> None:
    print("Login")


@register.on_click
def register_clicked() -> None:
    print("Register")


@save.on_click
def save_clicked() -> None:
    print("Save")


@delete.on_click
def delete_clicked() -> None:
    print("Delete")


layout.register(account_loop)
