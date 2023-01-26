from enum import Enum, auto

import pygame as pg
from sprite import Sprite

from . import GameLoop, Widget


class Mode(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class Layout(Widget):
    mode: Mode
    padding: int
    widgets: list[Widget]

    def __init__(
        self,
        rect: pg.rect.Rect,
        mode: Mode = Mode.HORIZONTAL,
        padding: int = 5,
    ) -> None:
        super().__init__(rect)

        self.mode = mode
        self.padding = padding
        self.widgets = []

        self.update()

    def add_widgets(self, *widgets: Widget) -> None:
        self.widgets += list(widgets)

    def register(self, loop: GameLoop) -> GameLoop:
        for sprite in self.widgets:
            sprite.register(loop)
        return loop

    def update(self) -> None:
        self.image = pg.surface.Surface(self.rect.size, pg.SRCALPHA)

        if len(self.widgets) <= 0:
            return

        if self.mode == Mode.HORIZONTAL:
            height = (
                self.rect.height // len(self.widgets)
                - (len(self.widgets) - 1) * self.padding
            )
            for n, widget in enumerate(self.widgets):
                widget.rect.x = self.rect.x
                widget.rect.y = self.rect.y
                widget.rect.width = self.rect.width
                widget.rect.height = height

                rel_rect = widget.rel_rect
                rel_rect.x = 0
                rel_rect.y = (height + self.padding) * n
                widget.rel_rect = rel_rect

                widget.update()
                self.image.blit(widget.image, rel_rect)
        elif self.mode == Mode.VERTICAL:
            width = (
                self.rect.width // len(self.widgets)
                - (len(self.widgets) - 1) * self.padding
            )
            for n, widget in enumerate(self.widgets):
                widget.rect.x = self.rect.x
                widget.rect.y = self.rect.y
                widget.rect.width = width
                widget.rect.height = self.rect.height

                rel_rect = widget.rel_rect
                rel_rect.x = (width + self.padding) * n
                rel_rect.y = 0
                widget.rel_rect = rel_rect

                widget.update()
                self.image.blit(widget.image, rel_rect)
