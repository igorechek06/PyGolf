from typing import Callable

import pygame as pg

from . import Font, GameLoop, Widget

FUNC = Callable[[], None]


class Button(Widget):
    text: str
    font: Font

    on_click_handler: FUNC | None

    def __init__(self, rect: pg.rect.Rect, text: str, font: Font | None = None) -> None:
        super().__init__(rect)

        self.text = text
        self.font = Font() if font is None else font

        self.on_click_handler = None

        self.update()

    def on_click(self) -> Callable[[FUNC], FUNC]:
        def wrapper(func: FUNC) -> FUNC:
            self.on_click_handler = func
            return func

        return wrapper

    def register(self, loop: GameLoop) -> GameLoop:
        def mouse_event(event: pg.event.Event) -> None:
            if (
                self.on_click_handler is not None
                and event.button == 1
                and self.rect.collidepoint(event.pos)
            ):
                self.on_click_handler()

        loop.add_event_handler(mouse_event, pg.MOUSEBUTTONUP)

        return loop

    def update(self) -> None:
        self.image = pg.surface.Surface(self.rect.size, pg.SRCALPHA)

        text_surface = pg.font.Font(self.font.name, self.font.size).render(
            self.text,
            self.font.antialias,
            self.font.color,
            self.font.background_color,
        )
        text_rect = text_surface.get_rect()

        pg.draw.rect(self.image, self.font.color, ((0, 0), self.rect.size), 5, 10)
        self.image.blit(
            text_surface,
            (
                (self.rect.width - text_rect.width) // 2,
                (self.rect.height - text_rect.height) // 2,
            ),
        )
