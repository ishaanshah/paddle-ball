import os
import sys
import termios
import atexit

from select import select


class KBHit:
    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~
                            termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Disable cursor
        print("\x1b[?25l")

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        ''' Resets to normal terminal.
        '''
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

        # Enable cursor
        print("\x1b[?25h")

    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
        '''
        return sys.stdin.read(1)

    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        dr, _, _ = select([sys.stdin], [], [], 0)
        return dr != []
