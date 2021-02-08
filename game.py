import brick
import shutil
import time
import sys
import config
import random

from colorama import init, Fore, Back, Cursor
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
    screen = Window(ncols, nlines, f"{config.bkgd} ")

    brick_count = ncols // (config.brick["dim"][0]+3)
    bricks = []
    for i in range(6):
        layer = []

        for j in range(brick_count):
            # Make 10% of bricks unbreakable
            strength = (i % 3) + 1
            if random.randrange(100) < 10:
                strength = 4

            if i % 2 == 0:
                layer.append(brick.Brick(
                    j*(config.brick["dim"][0]+3),
                    i*3, strength, screen
                ))
            else:
                dx = ncols % brick_count
                for j in range(brick_count):
                    layer.append(brick.Brick(
                        j*(config.brick["dim"][0]+3)+dx+3,
                        i*3, strength, screen
                    ))

        bricks.append(layer)

    for layer in bricks:
        for b in layer:
            b.update()

    screen.draw()
    sys.stdin.read(1)


if __name__ == "__main__":
    main()
