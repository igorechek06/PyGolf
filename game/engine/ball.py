from pygame.math import Vector2


class Ball:
    x: float
    y: float
    velocity: Vector2

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.velocity = Vector2()

    @property
    def pos(self) -> tuple[float, float]:
        return (self.x, self.y)
