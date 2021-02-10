import config

from object import Object
from typing import List


class Ball(Object):
    def __init__(self, x: int, y: int, speed: List[int], strength: int, screen):
        super().__init__(
            x, y, *config.ball["dim"],
            config.ball["color"], screen
        )
        self._speed = speed

    def move(self):
        nlines, ncols = self._screen.get_screen_size()

        # Check if x boundary has been crossed
        new_x = self._x + self._speed[0]
        if new_x >= 0 and new_x + self._width <= ncols:
            self._x = new_x
        else:
            self._speed[0] = -self._speed[0]

        # Check if y boundary has been crossed
        new_y = self._y + self._speed[1]
        if new_y >= 0 and new_y + self._height <= nlines:
            self._y = new_y
        else:
            self._speed[1] = -self._speed[1]
