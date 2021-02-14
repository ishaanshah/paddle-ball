import config

from object import Object


class PowerUp(Object):
    def __init__(self, screen):
        super().__init__(
            0, 0, *config.powerup["dim"],
            config.powerup["color"], screen, False
        )
        self.speed = config.powerup["speed"]

    def action(self, object):
        # What action should be performed by ther powerup
        # Override this method respective child classes
        pass

    def move(self, paddle, object):
        if self.active:
            nlines, _ = self._screen.get_screen_size()
            new_y = self.y + self.speed

            if int(new_y) + self.height > nlines:
                return False

            self.y = new_y

            # Check if powerup hit the paddle
            if (int(self.y + self.height) > paddle.y and
                    self.y < paddle.y + paddle.height and
                    self.x + self.width > paddle.x and
                    self.x < paddle.x + paddle.width):
                self.action(object)
                return False

        return True


class ExpandPaddle(PowerUp):
    def action(self, paddle):
        paddle.powerups = 'expand'
        paddle.set_width(int(config.paddle["dim"][0] * 1.5))


class ShrinkPaddle(PowerUp):
    def action(self, paddle):
        paddle.powerups = 'shrink'
        paddle.set_width(int(config.paddle["dim"][0] * 0.7))
