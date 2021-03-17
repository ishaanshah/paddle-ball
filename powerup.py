import config
import math

from object import Object
from ball import Ball


class PowerUp(Object):
    type = "base"
    start_tick = -1

    def __init__(self, color, screen):
        super().__init__(
            0, 0, *config.powerup["dim"],
            color, screen, False
        )
        self.speed = [0, 0]
        self.old_x = 0
        self.old_y = 0

    def action(self, object):
        # What action should be performed by ther powerup
        # Override this method respective child classes
        pass

    def move(self, paddle, object, tick):
        if self.active:
            nlines, ncols = self._screen.get_screen_size()
            self.speed[1] += (-config.ball["speed"][1] - self.speed[1]) / \
                config.powerup["gravity"]

            # Check if x boundary has been crossed
            new_x = self.x + self.speed[0]
            if new_x >= 0 and int(new_x) + self.width < ncols:
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

            self.y = new_y
            self.x = new_x

            # Check if powerup hit the paddle
            if (int(self.y + self.height) > paddle.y and
                    self.y < paddle.y + paddle.height and
                    self.x + self.width > paddle.x and
                    self.x < paddle.x + paddle.width):
                self.action(object)
                return False

        return True


class ExpandPaddle(PowerUp):
    type = "paddle"

    def __init__(self, screen):
        super().__init__(config.powerup["color"]["expand"], screen)

    def action(self, paddle):
        paddle.powerup = ["expand", config.powerup["duration"]]
        paddle.set_width(int(config.paddle["dim"][0] * 1.5))


class ShrinkPaddle(PowerUp):
    type = "paddle"

    def __init__(self, screen):
        super().__init__(config.powerup["color"]["shrink"], screen)

    def action(self, paddle):
        paddle.powerup = ["shrink", config.powerup["duration"]]
        paddle.set_width(int(config.paddle["dim"][0] * 0.7))


class FastBall(PowerUp):
    type = "ball"

    def __init__(self, screen):
        super().__init__(config.powerup["color"]["fast"], screen)

    def action(self, balls):
        for ball in balls:
            ball.powerup = ["fast", config.powerup["duration"]]
            ball.speed[0] = (ball.speed[0] / abs(ball.speed[0])) * \
                (abs(config.ball["speed"][0]) * 1.3)
            ball.speed[1] = (ball.speed[1] / abs(ball.speed[1])) * \
                (abs(config.ball["speed"][1]) * 1.3)


class ThruBall(PowerUp):
    type = "ball"

    def __init__(self, screen):
        super().__init__(config.powerup["color"]["thru"], screen)

    def action(self, balls):
        for ball in balls:
            ball.powerup = ["thru", config.powerup["duration"]]


class GrabPaddle(PowerUp):
    type = "ball"

    def __init__(self, screen):
        super().__init__(config.powerup["color"]["grab"], screen)

    def action(self, balls):
        for ball in balls:
            ball.powerup = ["grab", config.powerup["duration"]]


class MultiplyBall(PowerUp):
    type = "ball"

    def __init__(self, screen):
        super().__init__(config.powerup["color"]["multiply"], screen)

    def action(self, balls):
        to_append = []
        for ball in balls:
            to_append.append(Ball(ball.x, ball.y, [-ball.speed[0], ball.speed[1]],
                                  1, ball._screen))

        for ball in to_append:
            ball.paused = False
            if balls[0].powerup:
                ball.powerup = list(balls[0].powerup)

        balls += to_append[:max(0, 8 - len(balls))]
