from enum import Enum

import pygame as pg
import models as course
from tkinter import filedialog


class EditorState(Enum):
    start = 1
    finish = 2
    walls = 3
    friction_zone = 4
    dead_zone = 5


def render_course(surface: pg.surface.Surface, crs: course.Course) -> None:
    pg.draw.circle(surface, "white", crs.start.point, 10)
    pg.draw.circle(surface, "green", crs.finish.point, 10)

    for zone in crs.zone:
        if isinstance(zone, course.FrictionZone):
            color = "yellow"
        elif isinstance(zone, course.DeadZone):
            color = "red"
        pg.draw.rect(surface, color, pg.Rect(zone.pos.point, zone.size.size))

    for wall in crs.walls:
        pg.draw.line(surface, "gray", wall.start.point, wall.end.point, 5)


def render_preview(
    surface: pg.surface.Surface,
    p1: course.Point,
    p2: course.Point,
    state: EditorState,
) -> None:
    if state == EditorState.walls:
        pg.draw.line(surface, "gray", p1.point, p2.point, 5)
    if state in (EditorState.friction_zone, EditorState.dead_zone):
        if state == EditorState.friction_zone:
            color = "yellow"
        if state == EditorState.dead_zone:
            color = "red"
        pg.draw.rect(
            surface,
            color,
            (min(p1.x, p2.x), min(p1.y, p2.y), abs(p1.x - p2.x), abs(p1.y - p2.y)),
        )


pg.init()
window = pg.display.set_mode((750, 750), pg.RESIZABLE)

clock = pg.time.Clock()

crs = course.Course(
    friction=0.2,
    size=course.Size(width=500, height=500),
    start=course.Point(x=50, y=450),
    finish=course.Point(x=450, y=50),
)

current_state = EditorState.start
current_point = None

surface = pg.surface.Surface(crs.size.size)

while True:
    sx = (window.get_width() - surface.get_width()) // 2
    sy = (window.get_height() - surface.get_height()) // 2

    window.fill("grey")
    surface.fill("black")

    for e in pg.event.get():
        if e.type == pg.MOUSEBUTTONDOWN and e.button == pg.BUTTON_LEFT:
            if current_state == EditorState.start:
                crs.start.x = e.pos[0] - sx
                crs.start.y = e.pos[1] - sy
            if current_state == EditorState.finish:
                crs.finish.x = e.pos[0] - sx
                crs.finish.y = e.pos[1] - sy
            if current_state in (
                EditorState.walls,
                EditorState.dead_zone,
                EditorState.friction_zone,
            ):
                if current_point is None:
                    current_point = (e.pos[0] - sx, e.pos[1] - sy)

        if e.type == pg.MOUSEBUTTONUP and e.button == pg.BUTTON_LEFT:
            if current_point is not None:
                if current_state == EditorState.walls:
                    crs.walls.append(
                        course.Wall(
                            color=course.Color(r=75,g=75,b=75),
                            start=course.Point(
                                x=e.pos[0] - sx,
                                y=e.pos[1] - sy,
                            ),
                            end=course.Point(
                                x=current_point[0],
                                y=current_point[1],
                            ),
                        ),
                    )
                if current_state in (
                    EditorState.friction_zone,
                    EditorState.dead_zone,
                ):
                    pos = course.Point(
                        x=min(e.pos[0] - sx, current_point[0]),
                        y=min(e.pos[1] - sy, current_point[1]),
                    )
                    size = course.Size(
                        width=abs(e.pos[0] - sx - current_point[0]),
                        height=abs(e.pos[1] - sy - current_point[1]),
                    )
                    if current_state == EditorState.friction_zone:
                        crs.zone.append(
                            course.FrictionZone(friction=2, pos=pos, size=size),
                        )
                    if current_state == EditorState.dead_zone:
                        crs.zone.append(course.DeadZone(pos=pos, size=size))

                current_point = None

        if e.type == pg.KEYDOWN:
            if e.key == pg.K_DELETE:
                if current_state == EditorState.walls and len(crs.walls) > 0:
                    crs.walls.pop()
                if (
                    current_state == EditorState.dead_zone
                    or current_state == EditorState.friction_zone
                ) and len(crs.zone) > 0:
                    crs.zone.pop()

            if e.key == pg.K_RETURN:
                f = filedialog.asksaveasfile("w", filetypes=[('PyGolf Level', '*.pygolf')])
                if f is not None:
                    f.write(crs.json())
                    f.close()
                    pg.event.clear(pg.KEYDOWN)

            if e.key == pg.K_1:
                current_state = EditorState.start
            if e.key == pg.K_2:
                current_state = EditorState.finish
            if e.key == pg.K_3:
                current_state = EditorState.walls
            if e.key == pg.K_4:
                current_state = EditorState.friction_zone
            if e.key == pg.K_5:
                current_state = EditorState.dead_zone

        if e.type == pg.QUIT:
            exit()

    render_course(surface, crs)
    if current_point is not None:
        render_preview(
            surface,
            course.Point(x=current_point[0], y=current_point[1]),
            course.Point(x=pg.mouse.get_pos()[0] - sx, y=pg.mouse.get_pos()[1] - sy),
            current_state
        )

    window.blit(surface, (sx, sy))

    clock.tick(60)
    pg.display.flip()
