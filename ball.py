import config
import math

from object import Object
from typing import List


class Ball(Object):
    def __init__(self, x: int, y: int, speed: List[int], strength: int, screen):
        super().__init__(
            x, y, *config.ball["dim"],
            config.ball["color"], screen
        )
        self.old_x = x
        self.old_y = y
        self.speed = speed

    def move(self, bricks: list):
        nlines, ncols = self._screen.get_screen_size()

        # Check if x boundary has been crossed
        new_x = self.x + self.speed[0]
        if new_x >= 0 and int(new_x) + self.width <= ncols:
            if math.fabs(self.old_x - new_x) >= 1.0:
                self.old_x = int(self.x)
            self.x = new_x
        else:
            self.speed[0] = -self.speed[0]

        # Check if y boundary has been crossed
        new_y = self.y + self.speed[1]
        if new_y >= 0 and int(new_y) + self.height <= nlines:
            if math.fabs(self.old_y - new_y) >= 1.0:
                self.old_y = int(self.y)
            self.y = new_y
        else:
            self.speed[1] = -self.speed[1]

    def revert_pos(self):
        self.x = self.old_x
        self.y = self.old_y
