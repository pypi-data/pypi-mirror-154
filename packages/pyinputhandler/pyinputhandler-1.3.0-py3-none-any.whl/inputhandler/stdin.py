# getwch code based on code from jfktrey on GitHub: https://gist.github.com/jfktrey/8928865
# try_read code based on this answer on stackoverflow: https://stackoverflow.com/a/5047058
import platform


if platform.system() == "Windows":
    import msvcrt

    def getwch() -> str:
        '''
        Cross platform version of `getwch()`.

        Wide variant of `getch()`, returning a Unicode value.
        '''

        return msvcrt.getwch()

    def try_read() -> str:
        '''
        Tries to read the next character in the stdin buffer and return it. If there is none then it
        returns an empty string.
        '''
        try:
            msvcrt.ungetwch("\n")
            msvcrt.getwch()
            return ""
        except OSError:
            return msvcrt.getwch()
else:
    import tty
    import termios
    import sys
    import fcntl
    import os

    def getwch() -> str:
        '''
        Cross platform version of `getwch()`.

        Wide variant of `getch()`, returning a Unicode value.
        '''

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        return char

    def try_read() -> str:
        '''
        Tries to read the next character in the stdin buffer and return it. If there is none then it
        returns an empty string.
        '''
        fd = sys.stdin.fileno()
        old_attr = termios.tcgetattr(fd)
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)

        try:
            tty.setraw(fd)
            sys.stdin.read(1)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_attr)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)

        return char
