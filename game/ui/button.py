from typing import Callable

import pygame as pg
from pydantic import BaseModel

from . import GameLoop


class Font(BaseModel):
    name: str | None = None
    size: int = 50
    antialias: bool = True
    color: tuple[int, int, int] = (255, 255, 255)
    background_color: tuple[int, int, int] | None = None


class Button:
    x: int
    y: int
    font: Font
    text: pg.surface.Surface

    max_size: tuple[int | None, int | None]
    min_size: tuple[int | None, int | None]

    handlers: list[Callable[[], None]]

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        font: Font | None = None,
        min_size: tuple[int | None, int | None] = (None, None),
        max_size: tuple[int | None, int | None] = (None, None),
    ) -> None:
        self.x = x
        self.y = y
        self.font = Font() if font is None else font
        self.text = pg.font.Font(self.font.name, self.font.size).render(
            text,
            self.font.antialias,
            self.font.color,
            self.font.background_color,
        )

        self.max_size = max_size
        self.min_size = min_size

        self.handlers = []

    def get_rect(self) -> pg.rect.Rect:
        text_rect = self.text.get_rect()
        return pg.rect.Rect(
            self.x,
            self.y,
            max(
                min(text_rect.width, self.max_size[0] or float("inf")),
                self.min_size[0] or float("-inf"),
            ),
            max(
                min(text_rect.height, self.max_size[1] or float("inf")),
                self.min_size[1] or float("-inf"),
            ),
        )

    def show(self, screen: pg.surface.Surface) -> None:
        text_rect = self.text.get_rect()
        rect = self.get_rect()

        button = pg.surface.Surface(rect.size, pg.SRCALPHA)
        pg.draw.rect(button, self.font.color, ((0, 0), rect.size), 5, 10)
        button.blit(
            self.text,
            (
                (rect.width - text_rect.width) // 2,
                (rect.height - text_rect.height) // 2,
            ),
        )

        screen.blit(button, rect)

    def add_handler(self, func: Callable[[], None]) -> Callable[[], None]:
        self.handlers.append(func)
        return func

    def connect_game_loop(self, loop: GameLoop) -> None:
        loop.add_event_handler(self.__loop_event, pg.MOUSEBUTTONUP)

    def __loop_event(self, event: pg.event.Event) -> None:
        if event.button == 1 and self.get_rect().collidepoint(event.pos):
            for handler in self.handlers:
                handler()


class Layout:
    rect: pg.rect.Rect
    padding: int
    buttons: list[Button]

    def __init__(self, rect: pg.rect.Rect, padding: int = 5) -> None:
        self.rect = rect
        self.padding = padding
        self.buttons = []

    def add(self, *buttons: Button) -> None:
        self.buttons += list(buttons)

    def show(self, surface: pg.surface.Surface):
        assert len(self.buttons) >= 1, "No buttons in layout"
        layout = pg.surface.Surface(self.rect.size)

        min_size = (
            self.rect.width,
            self.rect.height // len(self.buttons)
            - self.padding * (len(self.buttons) - 1),
        )
        for n, button in enumerate(self.buttons):
            button.min_size = min_size
            button.x = 0
            button.y = (self.rect.height // len(self.buttons) + self.padding) * n
            button.show(layout)

        surface.blit(layout, self.rect)

    def connect_game_loop(self, loop: GameLoop) -> None:
        for button in self.buttons:
            button.connect_game_loop(loop)
