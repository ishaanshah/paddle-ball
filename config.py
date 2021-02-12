from colorama import Back

aspect_ratio = (16, 9)

bkgd = Back.BLACK

tick_interval = 0.01

brick = {
    "dim": (12, 2),
    "color": {
        1: Back.GREEN,
        2: Back.YELLOW,
        3: Back.RED,
        4: Back.BLUE
    }
}

paddle = {
    "dim": (25, 1),
    "color": Back.MAGENTA,
    "speed": 2
}

ball = {
    "dim": (2, 1),
    "color": Back.CYAN,
    "speed": [0.3, -0.3],
}

powerup = {
    "dim": (4, 1),
    "color": Back.WHITE,
    "speed": 1.5
}
