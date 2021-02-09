import config

from colorama import Back
from object import Object


class Paddle(Object):
    def __init__(self, x: int, y: int, screen):
        super().__init__(
            x, y, *config.paddle["dim"],
            config.paddle["color"], screen
        )

    def move(self, direction: int):
        pass
