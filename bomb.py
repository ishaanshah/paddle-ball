import config
import math

from object import Object
from typing import List


class Bomb(Object):
    def __init__(self, x: int, y: int, speed: int, screen):
        super().__init__(
            x, y, *config.bomb["dim"],
            config.bomb["color"], screen
        )
        self.speed = speed

    def move(self, paddle):
        # Check if top boundary has been crossed
        nrows, _ = self._screen.get_screen_size()
        new_y = self.y + self.speed

        # Check if bottom boundary is hit
        if int(new_y + self.height) > nrows:
            return False, False

        self.y = new_y

        pos_x = int(self.x)
        pos_y = int(self.y)
        hit = False
        res = True

        # Check if bomb hit any of the paddle
        if (pos_x < paddle.x + paddle.width and
            pos_x + self.width > paddle.x and
            pos_y < paddle.y + paddle.height and
                pos_y + self.height > paddle.y):

            hit = True
            res = False

        return res, hit
