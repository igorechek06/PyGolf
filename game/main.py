import pygame as pg
import ui


import game
import editor

pg.init()

window = pg.display.set_mode((720, 720))
clock = pg.time.Clock()

play_button = ui.Button("Играть", 147, 335, 200, 50, 36)
editor_button = ui.Button("Редактор", 388, 335, 200, 50, 36)

while True:
    window.fill("black")

    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()

        if e.type == pg.MOUSEBUTTONUP and e.button == 1:
            if play_button.rect.collidepoint(e.pos):
                game.run(window)
            if editor_button.rect.collidepoint(e.pos):
                editor.run(window)

    play_button.blit(window)
    editor_button.blit(window)

    pg.display.flip()
    clock.tick(60)
