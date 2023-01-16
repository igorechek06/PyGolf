import pygame as pg


class Button:
    text: str
    x: int
    y: int
    width: int
    height: int
    font_size: int

    def __init__(self, text: str, x: int, y: int, width: int, height: int, font_size: int) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.x, self.y, self.width, self.height)

    def blit(self, surface: pg.surface.Surface) -> None:
        pg.draw.rect(
            surface,
            "black",
            (self.x, self.y, self.width, self.height),
        )

        pg.draw.rect(
            surface,
            "white",
            (self.x, self.y, self.width, self.height),
            width=2,
        )

        font = pg.font.Font(None, self.font_size)
        text = font.render(self.text, True, "white")

        surface.blit(
            text,
            (
                self.x + (self.width - text.get_width()) // 2,
                self.y + (self.height - text.get_height()) // 2,
            ),
        )
