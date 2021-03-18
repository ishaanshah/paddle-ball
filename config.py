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
    },
    "speed": 0.003
}

paddle = {
    "dim": (30, 1),
    "color": Back.MAGENTA,
    "speed": 2
}

ball = {
    "dim": (2, 1),
    "color": Back.CYAN,
    "speed": [0.15, -0.15],
}

powerup = {
    "dim": (2, 1),
    "color": {
        "shrink": Back.LIGHTRED_EX,
        "expand": Back.LIGHTBLUE_EX,
        "fast": Back.LIGHTMAGENTA_EX,
        "multiply": Back.LIGHTYELLOW_EX,
        "thru": Back.LIGHTWHITE_EX,
        "grab": Back.LIGHTGREEN_EX,
        "shoot": Back.LIGHTBLACK_EX
    },
    "duration": 500,
    "gravity": 70,
}

bullet = {
    "dim": (1, 1),
    "color": Back.WHITE,
    "speed": -0.15,
    "rate": 200
}

boss = {
    "color": Back.RED
}

bomb = {
    "color": Back.LIGHTRED_EX,
    "speed": 0.15,
    "rate": 500,
    "dim": (1, 1)
}
