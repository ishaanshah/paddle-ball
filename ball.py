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
        self.paused = True
        self.old_x = x
        self.old_y = y
        self.speed = speed
        self.powerup = None

    def move(self, bricks: list, paddle):
        if self.paused:
            return True

        nlines, ncols = self._screen.get_screen_size()

        # Check if x boundary has been crossed
        new_x = self.x + self.speed[0]
        if new_x >= 0 and int(new_x) + self.width <= ncols:
            if math.fabs(self.old_x - new_x) >= 1.0:
                self.old_x = int(self.x)
            self.x = new_x
        else:
            self.speed[0] = -self.speed[0]

        # Check if top boundary has been crossed
        new_y = self.y + self.speed[1]
        if new_y >= 0:
            if math.fabs(self.old_y - new_y) >= 1.0:
                self.old_y = int(self.y)
            self.y = new_y
        else:
            self.speed[1] = -self.speed[1]

        # Check if bottom boundary is hit
        if int(new_y) + self.height > nlines:
            return False

        pos_x = int(self.x)
        pos_y = int(self.y)
        hit = False
        # Check if ball hit the paddle
        if (pos_y + self.height > paddle.y and
                pos_y < paddle.y + paddle.height and
                pos_x + self.width > paddle.x and
                pos_x < paddle.x + paddle.width):
            speed_sq = self.speed[0]**2 + self.speed[1]**2
            dvx = min(abs(paddle.x - pos_x),
                      abs(paddle.x + paddle.width - pos_x)) / (paddle.width*2)
            dvx = 1 - dvx
            self.speed[0] = (
                self.speed[0] / abs(self.speed[0])) * dvx * (speed_sq**0.5)
            self.speed[1] = -((abs(speed_sq - self.speed[0]**2))**0.5)

            # Revert position
            self.x = self.old_x
            self.y = self.old_y

            if self.powerup == "grab":
                self.paused = True

            hit = True

        # Check if ball hit any of the brick
        to_delete = None
        for y, layer in enumerate(bricks):
            if hit:
                break
            for x, brick in enumerate(layer):
                if (pos_x < brick.x + brick.width and
                        pos_x + self.width > brick.x and
                        pos_y < brick.y + brick.height and
                        pos_y + self.height > brick.y):

                    # Get direction of collision
                    pos_x = self.old_x
                    pos_y = self.old_y
                    if (brick.y >= pos_y + self.height or
                            brick.y + brick.height <= pos_y):
                        if not self.powerup == "thru":
                            self.speed[1] = -self.speed[1]
                    else:
                        if not self.powerup == "thru":
                            self.speed[0] = -self.speed[0]

                    # Revert position
                    self.x = self.old_x
                    self.y = self.old_y
                    if brick.hit_brick(self.powerup == "thru"):
                        to_delete = (y, x)

                    hit = True
                    break

        if to_delete:
            del bricks[to_delete[0]][to_delete[1]]

        return True
