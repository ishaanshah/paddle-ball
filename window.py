import sys
import termios
import tty

from colorama import Cursor


class Window():
    def __init__(self, ncols: int, nlines: int, bkgd: str):
        # Set class properties
        self._ncols = ncols
        self._nlines = nlines
        self._bkgd = bkgd

        # Initialise screen of with 'bkgd'
        self._content = [[bkgd for i in range(ncols)] for j in range(nlines)]

        fd = sys.stdin
        # Hide cursor
        print("\x1b[?25l")

        # Store old config to restore later
        self._old_attr = termios.tcgetattr(fd.fileno())

        # Disable echo
        new = termios.tcgetattr(fd.fileno())
        new[3] = new[3] & ~termios.ECHO
        termios.tcsetattr(fd.fileno(), termios.TCSADRAIN, new)

        # Set terminal to raw mode
        tty.setcbreak(fd, when=termios.TCSADRAIN)

    def __del__(self):
        # Reset terminal config
        termios.tcsetattr(sys.stdin.fileno(),
                          termios.TCSADRAIN, self._old_attr)

        # Show cursor
        print("\x1b[?25h")

    def clear(self):
        self._content = [[self._bkgd for i in range(
            self._ncols)] for j in range(self._nlines)]

    def addch(self, y: int, x: int, ch: str):
        self._content[y][x] = ch

    def draw(self):
        output = ""
        for y, line in enumerate(self._content):
            for x, char in enumerate(line):
                output += f"{Cursor.POS(x+1, y+1)}{char}"

        sys.stdout.write(output)

    def get_screen_size(self):
        return (self._nlines, self._ncols)
