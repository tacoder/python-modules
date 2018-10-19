#!/usr/bin/python
import sys,os
import curses
import json
import string

from curses_modules.filtering_menu  import FilteringMenu
import curses
import logging, logging.config
logger = logging.getLogger(__name__)

def isAlpha(asciiInt):
    return asciiInt in  [ord(c) for c in string.printable]

def draw_menu(stdscr):
    k=0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    menuItems = []

    for number in range(1,5):
        menuItems+=[{"menuDesc":"LONG NAME FOR AN ITEM item number" + str(number)}]
    m = FilteringMenu(stdscr,menuItems)
    m.render()

#    m.increaseOffset()


    # Loop where k is the last character pressed
    while (k != ord('q')):
        logger.debug("Key pressed : " + str(k))
        logger.debug(k)
        logger.debug(k == 10    )

        # Initialization
        # stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            m.down()
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            m.up()
            cursor_y = cursor_y - 1
        elif k == curses.KEY_NPAGE:
            m.pagedown()
        elif k == curses.KEY_PPAGE:
            m.pageup()
            cursor_x = cursor_x - 1
        elif k == curses.KEY_BACKSPACE or k ==127:
            m.removeSearchCh()
        elif k == curses.KEY_ENTER or k == 10:
            logger.debug("Retunging k yooo")
            return m.getCurrentlySelectedItem()
        elif isAlpha(k):
            m.addSearchCh(str(unichr(k)))

        logger.debug("curses.KEY_ENTER" + str(curses.KEY_ENTER))
        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    if "-debug" in sys.argv:
        print "Enabling logs"
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
    output = curses.wrapper(draw_menu)
    print "user selected " + str(output)

if __name__ == "__main__":
    main()
