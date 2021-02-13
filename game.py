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
from powerup import ExpandPaddle


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
    powerups = []
    for i in range(6):
        layer = []

        unbrkbl_brk_cnt = 0
        for j in range(brick_count):
            # Make 10% of bricks unbreakable
            strength = (i % 3) + 1
            if random.randrange(100) < 20 and unbrkbl_brk_cnt < brick_count // 2:
                strength = 4
                unbrkbl_brk_cnt += 1

            powerup = ExpandPaddle(screen)
            powerups.append(powerup)
            strength = 1
            if i % 2 == 0:
                layer.append(Brick(
                    j*(config.brick["dim"][0]+5),
                    i*5, strength, screen, powerup
                ))
            else:
                dx = ncols % brick_count
                layer.append(Brick(
                    j*(config.brick["dim"][0]+5)+dx+5,
                    i*5, strength, screen, powerup
                ))

        bricks.append(layer)

    # Create and draw the paddle
    paddle = Paddle(((ncols-1) - config.paddle["dim"][0]) // 2,
                    nlines-3, screen)

    # Create and draw the ball
    balls = [Ball((ncols-1) // 2 - 1, nlines-4,
                  config.ball["speed"], 1, screen)]

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

            last_update = time.time()

            # Clear screen
            screen.clear()

            # Move the paddle
            paddle.move(direction)

            # Move the powerups
            powerups = [powerup for powerup in powerups
                        if powerup.move(paddle)]

            # Move the ball
            balls = [ball for ball in balls if ball.move(bricks, paddle)]

            # Update bricks
            for layer in bricks:
                for brick in layer:
                    brick.update()

            # Update paddle
            paddle.update()

            # Update powerups
            for powerup in powerups:
                powerup.update()

            # Update ball
            for ball in balls:
                ball.update()

            screen.draw()

    f.close()


if __name__ == "__main__":
    main()
