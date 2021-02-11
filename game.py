import shutil
import time
import sys
import config
import random
import math

from colorama import init, Fore, Back, Cursor
from window import Window
from paddle import Paddle
from brick import Brick
from ball import Ball
from kbhit import KBHit


def main():
    random.seed(time.time())

    # Initialise colorama
    init()

    # Clear screen
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')

    # Get terminal size
    (ncols, nlines) = shutil.get_terminal_size()

    # Initialise screen
    screen = Window(ncols, nlines, f"{config.bkgd} ")

    # Initialise keyboard
    kb = KBHit()

    # Create and draw bricks
    brick_count = ncols // (config.brick["dim"][0]+5)
    bricks = []
    for i in range(6):
        layer = []

        unbrkbl_brk_cnt = 0
        for j in range(brick_count):
            # Make 10% of bricks unbreakable
            strength = (i % 3) + 1
            if random.randrange(100) < 20 and unbrkbl_brk_cnt < brick_count // 2:
                strength = 4
                unbrkbl_brk_cnt += 1

            if i % 2 == 0:
                layer.append(Brick(
                    j*(config.brick["dim"][0]+5),
                    i*5, strength, screen
                ))
            else:
                dx = ncols % brick_count
                layer.append(Brick(
                    j*(config.brick["dim"][0]+5)+dx+5,
                    i*5, strength, screen
                ))

        bricks.append(layer)

    # Create and draw the paddle
    paddle = Paddle(((ncols-1) - config.paddle["dim"][0]) // 2,
                    nlines-3, screen)

    # Create and draw the ball
    ball = Ball((ncols-1) // 2 - 1, nlines-4, config.ball["speed"], 1, screen)

    f = open("log", "w")

    last_update = 0
    while True:
        if (time.time() - last_update > config.tick_interval):
            direction = 0
            if kb.kbhit():
                c = kb.getch()
                if ord(c) == 27:
                    break

                if c == 'a':
                    direction = -1
                elif c == 'd':
                    direction = 1

            hit = False
            # Check if ball hit the paddle
            if (ball.y + ball.height > paddle.y and
                    ball.x + ball.width > paddle.x and
                    ball.x < paddle.x + paddle.width):
                speed_sq = ball.speed[0]**2 + ball.speed[1]**2
                dvx = min(abs(paddle.x - ball.x),
                          abs(paddle.x + paddle.width - ball.x)) / (paddle.width*2)
                dvx = 1 - dvx
                ball.speed[0] = (
                    ball.speed[0] / abs(ball.speed[0])) * dvx * (speed_sq**0.5)
                ball.speed[1] = -((speed_sq - ball.speed[0]**2)**0.5)
                ball.revert_pos()

                hit = True

            # Check if ball hit any of the brick
            to_delete = None
            for y, layer in enumerate(bricks):
                if hit:
                    break
                for x, brick in enumerate(layer):
                    if (ball.x < brick.x + brick.width and
                            ball.x + ball.width > brick.x and
                            ball.y < brick.y + brick.height and
                            ball.y + ball.height > brick.y):

                        # Get direction of collision
                        if (brick.y >= ball.y + ball.height - 1 or
                                brick.y + brick.height - 1 <= ball.y):
                            ball.speed[1] = -ball.speed[1]
                        else:
                            ball.speed[0] = -ball.speed[0]

                        ball.revert_pos()
                        if brick.hit_brick(1):
                            to_delete = (y, x)

                        hit = True
                        break

            if to_delete:
                del bricks[to_delete[0]][to_delete[1]]

            if hit:
                continue

            last_update = time.time()

            # Clear screen
            screen.clear()

            # Update bricks
            for layer in bricks:
                for brick in layer:
                    brick.update()

            # Move and update paddle
            paddle.move(direction)
            paddle.update()

            # Move and update ball
            ball.move(bricks)
            ball.update()

            screen.draw()

    f.close()


if __name__ == "__main__":
    main()
