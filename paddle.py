import config

from colorama import Back
from object import Object


class Paddle(Object):
    def __init__(self, x: int, y: int, screen):
        super().__init__(
            x, y, *config.paddle["dim"],
            config.paddle["color"], screen
        )
        self.powerup = None

    def set_width(self, new_width: int):
        _, ncols = self._screen.get_screen_size()
        if int(self.x) + new_width > ncols:
            self.x = ncols - new_width

        self.width = new_width

    def move(self, direction: int, balls):
        _, ncols = self._screen.get_screen_size()

        # Check if paddle is at any of the edges
        new_x = self.x + (direction*config.paddle["speed"])
        if int(new_x) >= 0 and int(new_x) + self.width <= ncols:
            self.x = new_x

            # Move paused balls along with paddle
            for ball in balls:
                if ball.paused:
                    ball.x += direction*config.paddle["speed"]
