import random
from powerup import (ExpandPaddle, FastBall, GrabPaddle, MultiplyBall,
                     ShrinkPaddle, ThruBall, ShootPaddle)
import config

from brick import Brick


def level_one(screen):
    _, ncols = screen.get_screen_size()
    brick_count = (ncols - 30) // (config.brick["dim"][0]+5)
    bricks = []
    powerups = []
    for i in range(3):
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
                                              MultiplyBall, ShrinkPaddle, ThruBall, ShootPaddle])
                powerup = powerup_type(screen)
                powerups.append(powerup)

            layer.append(Brick(
                15+j*(config.brick["dim"][0]+5),
                i*5 + 1, strength, screen, powerup, rainbow
            ))

        bricks.append(layer)

    return bricks, powerups


def level_two(screen):
    _, ncols = screen.get_screen_size()
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
                                              MultiplyBall, ShrinkPaddle, ThruBall, ShootPaddle])
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

    return bricks, powerups


def level_three(screen):
    _, ncols = screen.get_screen_size()
    bricks = [[]]
    for i in range(3):
        bricks[0].append(
            Brick(i*(config.brick["dim"][0]+5),
                  15, 4, screen))

    for i in range(3):
        start = ncols - config.brick["dim"][0]
        bricks[0].append(
            Brick(start - i*(config.brick["dim"][0]+5),
                  15, 4, screen))

    return bricks, []
