import config

from colorama import Back
from object import Object


class Brick(Object):
    def __init__(self, x: int, y: int, strength: int, screen):
        super().__init__(
            x, y, *config.brick["dim"],
            config.brick["color"][strength], screen
        )
        self._strength = strength

    def hit_brick(self, ball_strength: int):
        pass
