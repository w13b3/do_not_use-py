import curses
import time
from curses import wrapper
from itertools import cycle

# constants
load_spin = cycle(("|", "/", "-", "\\"))

def setup():
    """ setup the terminal window rules for this curses session """
    stdscr = curses.initscr()
    curses.noecho()
    # stdscr.leaveok(True)
    stdscr.nodelay(True)
    stdscr.keypad(True)  # block incoming keys  https://docs.python.org/3/library/curses.html#curses.window.keypad
    # stdscr.nodelay(True)  # getch will be unblocking
    return stdscr


def colors():
    """ create colour pairs """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)


def cleanup(stdscr):
    """ cleanup after the program ran """
    # stdscr.ungetch()  # stop blocking
    stdscr.clear()  # clear the screen
    stdscr.erase()  # clear the window
    # stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    exit(0)


def move_cursor(stdscr, beep=False, move=True):
    key = None
    try:
        key = stdscr.getch()  # stdscr.leaveok(False) sets getch to non-blocking
    except KeyboardInterrupt:
        exit(0)

    height, width = stdscr.getmaxyx()  # get the size of the terminal
    cursor_y, cursor_x = stdscr.getyx()  # get the current cursor location

    curses.mousemask(curses.ALL_MOUSE_EVENTS)  # listen for mouse events
    expected_keys = (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_MOUSE)
    if key in expected_keys and bool(beep):
        curses.beep()  # show a beep or flash

    if bool(move):
        if key == curses.KEY_MOUSE:
            try:
                _, mx, my, _, _ = curses.getmouse()  # get the clicked location
                cursor_y, cursor_x = my, mx  # place of cursor
            except curses.error:  # prevents crash by fast clicking on window
                pass
        elif key == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif key == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif key == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif key == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

    # make sure the cursor doesn't leave the window
    cursor_x = max(0, cursor_x)
    cursor_x = min(width - 1, cursor_x)
    cursor_y = max(0, cursor_y)
    cursor_y = min(height - 1, cursor_y)

    # stdscr.move(cursor_y, cursor_x)  # move the cursor
    return cursor_y, cursor_x, key

def main(stdscr):
    cursor_y, cursor_x = 0, 0
    key = None
    stdscr.clear()  # clear the screen

    old_height, old_width = 0, 0
    while key != ord('q') != ord('Q'):
        height, width = stdscr.getmaxyx()  # get the size of the termina
        if old_height != height and old_width != width:
            old_height, old_width = height, width
            stdscr.clear()
        elif not old_height and not old_width:
            old_height, old_width = height, width

        cursor_y, cursor_x, key = move_cursor(stdscr)  # get latest cursor

        # need to check the width and the he


        # Rendering some text  (row, column, text)
        stdscr.addstr(0, 0, f"Terminal Width: {width}, Height: {height}", curses.color_pair(1))
        stdscr.addstr(1, 0, f"Cursor location x: {cursor_x}, y: {cursor_y}", curses.color_pair(2))

        stdscr.addstr(2, 0, "Spinner:", curses.color_pair(3))
        stdscr.addstr(f" {next(load_spin)}")

        stdscr.addstr(int(height/2), int(width/2), "O")

        stdscr.addstr(height - 1, 0, "press 'Q' to quit")

        stdscr.move(cursor_y, cursor_x)
        try:  # Refresh the screen
            stdscr.touchwin()
            curses.doupdate()
            curses.napms(10)
        except KeyboardInterrupt:
            break  # cleanup()


# __init__
stdscr = setup()
colors()  # create color pairs
wrapper(main)  # wrap the curses session in a try/except to cleanup after error also provides stdscr to given function

# __del__
cleanup(stdscr)  # cleanup
