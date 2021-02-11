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
        if self._strength == 4:
            return

        self._strength -= 1

        if self._strength == 0:
            return True

        self.set_color(config.brick["color"][self._strength])
        self.update()
        return False
