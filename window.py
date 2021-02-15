import sys

from colorama import Cursor


class Window():
    def __init__(self, x: int, y: int, ncols: int, nlines: int, bkgd: str):
        # Set class properties
        self._ncols = ncols
        self._nlines = nlines
        self._bkgd = bkgd
        self._x = x
        self._y = y

        # Initialise screen of with 'bkgd'
        self._content = [[bkgd for i in range(ncols)] for j in range(nlines)]

    def clear(self):
        self._content = [[self._bkgd for i in range(
            self._ncols)] for j in range(self._nlines)]

    def addch(self, y: int, x: int, ch: str):
        self._content[y][x] = ch

    def draw(self):
        output = ""
        for y, line in enumerate(self._content):
            for x, char in enumerate(line):
                output += f"{Cursor.POS(self._x + x + 1, self._y + y + 1)}{char}"

        sys.stdout.write(output)

    def get_screen_size(self):
        return (self._nlines, self._ncols)
