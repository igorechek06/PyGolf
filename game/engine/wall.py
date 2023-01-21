import pygame as pg

from . import Sprite

x, y = lambda p: p[0], lambda p: p[1]


class Wall(Sprite):
    color: tuple[int, int, int]
    points: list[tuple[int, int]]

    def __init__(
        self,
        color: tuple[int, int, int],
        points: list[tuple[int, int]],
    ) -> None:
        xmin, ymin = min(points, key=x)[0], min(points, key=y)[1]
        xmax, ymax = max(points, key=x)[0], max(points, key=y)[1]

        self.color = color
        self.points = [(p[0] - xmin, p[1] - ymin) for p in points]

        rect = pg.rect.Rect(xmin, ymin, xmax - xmin, ymax - ymin)
        image = pg.surface.Surface(rect.size, pg.SRCALPHA)
        pg.draw.polygon(image, self.color, self.points)

        super().__init__(image, rect)
