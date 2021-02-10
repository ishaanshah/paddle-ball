from colorama import Back

aspect_ratio = (16, 9)

bkgd = Back.BLACK

tick_interval = 0.01

brick = {
    "dim": (10, 1),
    "color": {
        1: Back.GREEN,
        2: Back.YELLOW,
        3: Back.RED,
        4: Back.BLUE
    }
}

paddle = {
    "dim": (18, 1),
    "color": Back.MAGENTA
}

ball = {
    "dim": (2, 1),
    "color": Back.CYAN
}
