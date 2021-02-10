import shutil
import time
import sys
import config
import random

from colorama import init, Fore, Back, Cursor
from window import Window
from paddle import Paddle
from brick import Brick
from ball import Ball


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

    # Create and draw bricks
    brick_count = ncols // (config.brick["dim"][0]+3)
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
                    j*(config.brick["dim"][0]+3),
                    i*3, strength, screen
                ))
            else:
                dx = ncols % brick_count
                layer.append(Brick(
                    j*(config.brick["dim"][0]+3)+dx+3,
                    i*3, strength, screen
                ))

        bricks.append(layer)

    # Create and draw the paddle
    paddle = Paddle(((ncols-1) - config.paddle["dim"][0]) // 2,
                    nlines-3, screen)

    # Create and draw the ball
    ball = Ball((ncols-1) // 2 - 1, nlines-4, [0.4, -0.4], 1, screen)

    last_update = 0
    while True:
        if (time.time() - last_update > config.tick_interval):
            last_update = time.time()

            # Clear screen
            screen.clear()

            # Update bricks
            for layer in bricks:
                for brick in layer:
                    brick.update()

            # Update paddle
            paddle.update()

            # Move and Update ball
            ball.move()
            ball.update()

            screen.draw()

    sys.stdin.read(1)


if __name__ == "__main__":
    main()
