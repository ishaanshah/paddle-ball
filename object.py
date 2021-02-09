import config

from typing import List, Tuple
from colorama import Cursor


class Object():
    def __init__(self, x, y, width, height, color, screen):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
        self._screen = screen
        self.update()

    def __del__(self):
        self._color = config.bkgd
        self.update()

    def update(self):
        for i in range(self._width):
            for j in range(self._height):
                x, y = self._x + i, self._y + j
                self._screen.addch(y, x, f"{self._color} ")

    def get_bound_box(self) -> List[Tuple[int]]:
        pass
