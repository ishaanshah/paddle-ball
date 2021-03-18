import math
import random
import shutil
import sys
import time

from colorama import Back, Cursor, Fore, init

import config
import levels
from ball import Ball
from bullet import Bullet
from kbhit import KBHit
from paddle import Paddle
from window import Window

# TODO: Fix paddle for shoot_paddle


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

    # Create and draw the paddle
    paddle = Paddle(((ncols-1) - config.paddle["dim"][0]) // 2,
                    nlines-4, screen)

    last_update = 0
    start = time.time()
    score = 0
    lives = 3
    curr_level = 1
    while curr_level <= 3:
        # Create and draw bricks
        if curr_level == 1:
            bricks, powerups = levels.level_one(screen)
        elif curr_level == 2:
            bricks, powerups = levels.level_two(screen)
        elif curr_level == 3:
            bricks, powerups = levels.level_one(screen)
        else:
            sys.exit()

        while lives:
            # Reset paddle location
            paddle.x = ((ncols-1) - config.paddle["dim"][0]) // 2
            paddle.powerup = None

            # Create and draw the ball
            balls = [Ball(random.randrange(paddle.x, paddle.x+paddle.width), nlines-5,
                          list(config.ball["speed"]), 1, screen)]

            # List to store bullets
            bullets = []
            shoot_paddle = [0]

            tick = 0
            while len(balls):
                if (time.time() - last_update > config.tick_interval):
                    tick += 1
                    for i in range(ncols):
                        print(f"{Cursor.POS(1+i, 1)}{Back.BLACK} ", end='')

                    statusline = f"{Cursor.POS(1, 1)}Level: {curr_level}   "
                    statusline += f"Score: {score}   "
                    statusline += f"Time: {int(time.time() - start)}   "
                    statusline += f"Lives: {lives}   "
                    statusline += f"Shoot Paddle: {int(shoot_paddle[0] * config.tick_interval)}   "
                    print(statusline, end='')

                    last_update = time.time()

                    change_level = False
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
                        elif c == '1' or c == '2' or c == '3':
                            curr_level = int(c) if curr_level != 3 else 4
                            change_level = True
                            break

                    # Create new bullets if needed
                    shoot_paddle[0] = max(0, shoot_paddle[0]-1)
                    if shoot_paddle[0] and shoot_paddle[0] % config.bullet["rate"] == 0:
                        bullets.append(
                            Bullet(max(paddle.x, 0), paddle.y,
                                   config.bullet["speed"], screen)
                        )
                        bullets.append(
                            Bullet(min(paddle.x + paddle.width, screen.get_screen_size()[1]-1),
                                   paddle.y, config.bullet["speed"], screen)
                        )

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
                        else:
                            object = shoot_paddle

                        if not powerup.move(paddle, object, tick):
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

                    # Move the bullets
                    to_delete = []
                    for bullet in bullets:
                        delete, d_score = bullet.move(bricks)
                        if not delete:
                            to_delete.append(bullet)

                        score += d_score

                    bullets = [
                        bullet for bullet in bullets if bullet not in to_delete
                    ]

                    # Update bricks
                    for layer in bricks:
                        for brick in layer:
                            brick.rainbow(tick)
                            brick.move(tick)
                            if brick.y + brick.height > paddle.y:
                                sys.exit()
                            brick.update()

                    # Update paddle
                    paddle.update()

                    # Update powerups
                    for powerup in powerups:
                        powerup.update()

                    # Update ball
                    for ball in balls:
                        ball.update()

                    # Update bullets
                    for bullet in bullets:
                        bullet.update()

                    screen.draw()

                    # Check if all breackable bricks are broken
                    change_level = True
                    for layer in bricks:
                        for brick in layer:
                            if brick._strength != 4:
                                change_level = False
                                break
                        if not change_level:
                            break

                    if change_level:
                        curr_level += 1
                        break

            if change_level:
                break

            lives -= 1


if __name__ == "__main__":
    main()
