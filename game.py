import math
import random
import shutil
import sys
import time

from colorama import Back, Cursor, Fore, init

import config
from ball import Ball
from brick import Brick
from kbhit import KBHit
from paddle import Paddle
from powerup import (ExpandPaddle, FastBall, GrabPaddle, MultiplyBall,
                     ShrinkPaddle, ThruBall)
from window import Window


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
    screen = Window(0, 1, ncols, nlines-1, f"{config.bkgd} ")

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

            # Make 20% of bricks rainbow
            rainbow = False
            if random.randrange(100) < 20 and strength < 4:
                rainbow = True

            # Make 30% of breackable bricks have a powerup
            powerup = None
            if strength < 4 and random.randrange(100) < 30:
                powerup_type = random.choice([ExpandPaddle, FastBall, GrabPaddle,
                                              MultiplyBall, ShrinkPaddle, ThruBall])
                powerup = powerup_type(screen)
                powerups.append(powerup)

            if i % 2 == 0:
                layer.append(Brick(
                    j*(config.brick["dim"][0]+5),
                    i*5 + 1, strength, screen, powerup, rainbow
                ))
            else:
                dx = ncols % brick_count
                layer.append(Brick(
                    j*(config.brick["dim"][0]+5)+dx+5,
                    i*5 + 1, strength, screen, powerup, rainbow
                ))

        bricks.append(layer)

    # Create and draw the paddle
    paddle = Paddle(((ncols-1) - config.paddle["dim"][0]) // 2,
                    nlines-4, screen)

    last_update = 0
    start = time.time()
    score = 0
    lives = 3
    while lives:
        # Reset paddle location
        paddle.x = ((ncols-1) - config.paddle["dim"][0]) // 2
        paddle.powerup = None

        # Create and draw the ball
        balls = [Ball(random.randrange(paddle.x, paddle.x+paddle.width), nlines-5,
                      list(config.ball["speed"]), 1, screen)]
        ticks = 0
        while len(balls):
            if (time.time() - last_update > config.tick_interval):
                ticks += 1
                for i in range(ncols):
                    print(f"{Cursor.POS(1+i, 1)}{Back.BLACK} ", end='')

                statusline = f"{Cursor.POS(1, 1)}Score: {score}   "
                statusline += f"Time: {int(time.time() - start)}   "
                statusline += f"Lives: {lives}"
                print(statusline, end='')

                direction = 0
                if kb.kbhit():
                    c = kb.getch()
                    if ord(c) == 27:
                        sys.exit(0)

                    if c == 'a':
                        direction = -1
                    elif c == 'd':
                        direction = 1
                    elif c == ' ':
                        # Activate balls
                        for ball in balls:
                            ball.paused = False

                last_update = time.time()

                # Clear screen
                screen.clear()

                # Move the paddle
                paddle.move(direction, balls)

                # Move the powerups
                to_delete = []
                for powerup in powerups:
                    object = None
                    if powerup.type == "paddle":
                        object = paddle
                    elif powerup.type == "ball":
                        object = balls

                    if not powerup.move(paddle, object):
                        to_delete.append(powerup)

                powerups = [
                    powerup for powerup in powerups
                    if powerup not in to_delete
                ]

                # Move the ball
                to_delete = []
                for ball in balls:
                    delete, d_score = ball.move(bricks, paddle)
                    if not delete:
                        to_delete.append(ball)

                    score += d_score

                balls = [ball for ball in balls if ball not in to_delete]

                # Update bricks
                for layer in bricks:
                    for brick in layer:
                        brick.rainbow(ticks)
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

        lives -= 1


if __name__ == "__main__":
    main()
