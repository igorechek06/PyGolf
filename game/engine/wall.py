from math import cos, sin, sqrt

import pygame as pg
from sprite import Sprite

x, y = lambda p: p[0], lambda p: p[1]


def line2poly(
    start: tuple[int, int],
    end: tuple[int, int],
    width: int,
) -> list[tuple[int, int]]:
    x, y = (start[0] - end[0]), (end[1] - start[1])
    c = sqrt(x**2 + y**2)
    dx, dy = int(width * cos(y / c)) // 2, int(width * sin(x / c)) // 2
    return [
        (start[0] - dx, start[1] - dy),
        (end[0] - dx, end[1] - dy),
        (end[0] + dx, end[1] + dy),
        (start[0] + dx, start[1] + dy),
    ]


class Wall(Sprite):
    points: list[tuple[int, int]]
    rel_points: list[tuple[int, int]]
    color: tuple[int, int, int]

    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: tuple[int, int, int],
        width: int = 5,
    ) -> None:
        points = line2poly(start, end, width)
        xmin, ymin = min(points, key=x)[0], min(points, key=y)[1]
        xmax, ymax = max(points, key=x)[0], max(points, key=y)[1]

        self.points = points
        self.rel_points = [(p[0] - xmin, p[1] - ymin) for p in self.points]
        self.color = color

        rect = pg.rect.Rect(xmin, ymin, xmax - xmin, ymax - ymin)
        image = pg.surface.Surface(rect.size, pg.SRCALPHA)
        pg.draw.polygon(image, self.color, self.rel_points)

        super().__init__(image, rect)

    def update(self) -> None:
        pass
