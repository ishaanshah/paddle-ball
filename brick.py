import config

from colorama import Back
from object import Object


class Brick(Object):
    def __init__(self, x: int, y: int, strength: int, screen, powerup=None, rainbow=False):
        super().__init__(
            x, y, *config.brick["dim"],
            config.brick["color"][strength], screen
        )
        self._strength = strength
        self._powerup = powerup
        self._rainbow = rainbow

        # Set powerup location
        if powerup:
            self._powerup.x = x + (config.brick["dim"][0] // 2)
            self._powerup.y = y + config.brick["dim"][1] - self._powerup.height

    def hit_brick(self, thru: bool):
        self._rainbow = False
        if self._strength == 4:
            return thru

        if thru:
            self._strength = 0
        else:
            self._strength -= 1

        if self._strength == 0:
            if self._powerup:
                self._powerup.active = True
            return True

        self.set_color(config.brick["color"][self._strength])
        return False

    def rainbow(self, tick):
        if self._rainbow and tick % 100 == 0:
            self._strength = (self._strength % 4) + 1
            self.set_color(config.brick["color"][self._strength])
