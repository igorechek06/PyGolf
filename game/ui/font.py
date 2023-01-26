from dataclasses import dataclass


@dataclass
class Font:
    name: str | None = None
    size: int = 50
    antialias: bool = True
    color: tuple[int, int, int] = (255, 255, 255)
    background_color: tuple[int, int, int] | None = None
