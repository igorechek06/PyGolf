from enum import Enum, auto
from re import Pattern
from typing import Callable

import pygame as pg

from . import Font, GameLoop, Widget


class Field(Widget):
    class Mode(Enum):
        IDLE = auto()
        TYPING = auto()

    MODE_CHANGED = Callable[[Mode], None]
    TEXT_CHANGED = Callable[[str], None]

    hint: str
    text: str
    regex: Pattern | None
    hide: bool
    font: Font
    mode: Mode

    on_text_changed_handler: TEXT_CHANGED | None
    on_mode_changed_handler: MODE_CHANGED | None

    def __init__(
        self,
        rect: pg.rect.Rect,
        hint: str,
        text: str = "",
        regex: Pattern | None = None,
        hide: bool = False,
        font: Font | None = None,
    ) -> None:
        super().__init__(rect)

        self.hint = hint
        self.regex = regex
        self.hide = hide
        self.font = Font() if font is None else font
        self.mode = self.Mode.IDLE

        self.on_text_changed_handler = None
        self.on_mode_changed_handler = None

        self.set_text(text)
        self.update()

    def set_text(self, text: str) -> None:
        if self.regex is not None:
            match = self.regex.match(text)
            if match is not None:
                self.text = match.group()
                self.update()
            elif not hasattr(self, "text"):
                raise ValueError("Text does not match regular expression")
        else:
            self.text = text
            self.update()
        if self.on_text_changed_handler:
            self.on_text_changed_handler(self.text)

    def set_mode(self, mode: Mode) -> None:
        self.mode = mode
        if self.on_mode_changed_handler is not None:
            self.on_mode_changed_handler(mode)

    def on_text_changed(self, func: TEXT_CHANGED) -> TEXT_CHANGED:
        self.on_text_changed_handler = func
        return func

    def on_mode_changed(self, func: MODE_CHANGED) -> MODE_CHANGED:
        self.on_mode_changed_handler = func
        return func

    def register(self, loop: GameLoop) -> GameLoop:
        def mouse_event(event: pg.event.Event) -> None:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.set_mode(self.Mode.TYPING)
                else:
                    self.set_mode(self.Mode.IDLE)
            self.update()

        def key_event(event: pg.event.Event) -> None:
            if self.mode == self.Mode.TYPING:
                text: str = event.unicode
                if text.isprintable():
                    self.set_text(self.text + text)
                elif event.key == pg.K_BACKSPACE:
                    self.set_text(self.text[:-1])
                elif event.key in (pg.K_ESCAPE, pg.K_RETURN):
                    self.set_mode(self.Mode.IDLE)

                self.update()

        loop.add_event_handler(mouse_event, pg.MOUSEBUTTONDOWN)
        loop.add_event_handler(key_event, pg.KEYDOWN)

        return loop

    def update(self) -> None:
        self.image = pg.surface.Surface(self.rect.size, pg.SRCALPHA)

        text_surface = pg.font.Font(self.font.name, self.font.size).render(
            ("*" * len(self.text) if self.hide else self.text)
            if len(self.text) >= 1 or self.mode == self.Mode.TYPING
            else self.hint,
            self.font.antialias,
            self.font.color,
            self.font.background_color,
        )
        text_rect = text_surface.get_rect()

        pg.draw.rect(self.image, self.font.color, ((0, 0), self.rect.size), 5, 10)
        text_rect = self.image.blit(
            text_surface, (20, (self.rect.height - text_rect.height) // 2)
        )

        if self.mode == self.Mode.TYPING:
            pg.draw.line(
                self.image,
                self.font.color,
                (text_rect.right, 20),
                (text_rect.right, self.rect.height - 20),
                2,
            )
