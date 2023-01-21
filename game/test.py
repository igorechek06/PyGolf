import pygame as pg

sprites = pg.sprite.Group()

ball = pg.sprite.Sprite(sprites)
ball.image = pg.transform.scale(pg.image.load("./src/sprites/ball.svg"), (50, 50))
ball.rect = pg.rect.Rect((0, 0), ball.image.get_size())

water = pg.sprite.Sprite(sprites)
water.image = pg.transform.scale(pg.image.load("./src/sprites/water.svg"), (100, 200))
water.rect = pg.rect.Rect((200, 200), water.image.get_size())

screen = pg.display.set_mode((500, 500))


while True:
    screen.fill("black")

    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()

    ball.rect.center = pg.mouse.get_pos()

    print(pg.sprite.collide_mask(ball, water) is not None)

    sprites.draw(screen)

    pg.display.update()
