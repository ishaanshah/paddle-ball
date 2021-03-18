import config
import math

from object import Object
from typing import List


class Bullet(Object):
    def __init__(self, x: int, y: int, speed: int, screen):
        super().__init__(
            x, y, *config.bullet["dim"],
            config.bullet["color"], screen
        )
        self.speed = speed

    def move(self, bricks: list):
        score = 0

        # Check if top boundary has been crossed
        new_y = self.y + self.speed

        # Check if bottom boundary is hit
        if int(new_y) < 0:
            return False, 0

        self.y = new_y

        pos_x = int(self.x)
        pos_y = int(self.y)
        hit = False

        # Check if bullet hit any of the brick
        to_delete = None
        for y, layer in enumerate(bricks):
            if hit:
                break
            for x, brick in enumerate(layer):
                if (pos_x < brick.x + brick.width and
                        pos_x + self.width > brick.x and
                        pos_y < brick.y + brick.height and
                        pos_y + self.height > brick.y):

                    if brick.hit_brick(False, [0, self.speed], 0):
                        to_delete = (y, x)
                        score += 10

                    hit = True
                    break

        if to_delete:
            del bricks[to_delete[0]][to_delete[1]]

        return not hit, score
