from typing import Callable, Generic, ParamSpec

import pygame as pg

S = ParamSpec("S")
EVENT = Callable[[pg.event.Event], None]


class GameLoop(Generic[S]):
    loop: Callable[S, None]
    finish: Callable[S, None] | None
    event_handlers: dict[int, list[EVENT]]

    def __init__(
        self,
        loop: Callable[S, None],
        finish: Callable[S, None] | None = None,
    ) -> None:
        self.loop = loop
        self.finish = finish
        self.event_handlers = {}

    def add_event_handler(self, func: EVENT, event_type: int) -> None:
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(func)

    def event_handler(self, event_type: int) -> Callable[[EVENT], EVENT]:
        def wrapper(func: EVENT) -> EVENT:
            self.add_event_handler(func, event_type)
            return func

        return wrapper

    def start(self, *args: S.args, **kwargs: S.kwargs) -> None:
        work = True

        while work:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    work = False

                if event.type in self.event_handlers:
                    for handler in self.event_handlers[event.type]:
                        handler(event)

            self.loop(*args, **kwargs)

        if self.finish is not None:
            self.finish(*args, **kwargs)
