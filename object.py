import config

from typing import List, Tuple
from colorama import Cursor


class Object():
    def __init__(self, x: int, y: int, width: int, height: int, color: str, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._color = color
        self._screen = screen
        self.update()

    def __repr__(self):
        return repr(f"{self.x} {self.y} {self.width} {self.height}")

    def __del__(self):
        self._color = config.bkgd
        self.update()

    def set_color(self, color: str):
        self._color = color

    def update(self):
        for i in range(self.width):
            for j in range(self.height):
                x, y = self.x + i, self.y + j
                self._screen.addch(int(y), int(x), f"{self._color} ")
