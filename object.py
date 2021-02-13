import config

from typing import List, Tuple
from colorama import Cursor


class Object():
    def __init__(self, x: int, y: int, width: int, height: int,
                 color: str, screen, active: bool = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._color = color
        self._screen = screen
        self.active = active
        self.update()

    def __repr__(self):
        return repr(f"{self.x} {self.y} {self.width} {self.height}")

    def set_color(self, color: str):
        self._color = color

    def update(self):
        if self.active:
            for i in range(self.width):
                for j in range(self.height):
                    x, y = self.x + i, self.y + j
                    self._screen.addch(int(y), int(x), f"{self._color} ")
