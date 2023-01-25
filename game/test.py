import pygame as pg

screen = pg.display.set_mode((500, 500))

walls: list[tuple[tuple[int, int], tuple[int, int]]] = []
prev: tuple[int, int] | None = None

while True:
    screen.fill("black")

    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                if prev is not None:
                    walls.append((prev, e.pos))
                    prev = None
                else:
                    prev = e.pos
            if e.button == 2:
                if prev is None:
                    walls.pop()
                else:
                    prev = None

    if prev is not None:
        pg.draw.line(screen, "gray", prev, pg.mouse.get_pos(), 5)

    for wall in walls:
        pg.draw.line(screen, "gray", wall[0], wall[1], 5)

    pg.display.update()
