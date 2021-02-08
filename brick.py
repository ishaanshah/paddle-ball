import config

from colorama import Back
from typing import List, Tuple
from object import Object


class Brick(Object):
    def __init__(self, x, y, strength, screen):
        super().__init__(
            x, y, *config.brick["dim"],
            config.brick["color"][strength], screen
        )
        self._strength = strength

    def hit_brick(self, ball_strength: int):
        pass
