import config

from object import Object
from ball import Ball


class PowerUp(Object):
    type = "base"

    def __init__(self, color, screen):
        super().__init__(
            0, 0, *config.powerup["dim"],
            color, screen, False
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
