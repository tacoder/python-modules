#!/usr/bin/python
import sys,os
import curses
import string
from curses_modules.filtering_menu  import FilteringMenu
import curses
import logging, logging.config
logger = logging.getLogger(__name__)

def isAlpha(asciiInt):
    return asciiInt in  [ord(c) for c in string.printable]

def draw_menu(stdscr, menuItems):
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    m = FilteringMenu(stdscr,menuItems)
    m.render()


    k=0
    # Loop where k is the last character pressed
    while (True):
        logger.debug("Key pressed : " + str(k))
        logger.debug(k)
        logger.debug(k == 10    )

        # Initialization
        # stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            m.down()
        elif k == curses.KEY_UP:
            m.up()
        elif k == curses.KEY_NPAGE:
            m.pagedown()
        elif k == curses.KEY_PPAGE:
            m.pageup()
        elif k == curses.KEY_BACKSPACE or k ==127:
            m.removeSearchCh()
        elif k == curses.KEY_ENTER or k == 10:
            logger.debug("Retunging.")
            return m.getCurrentlySelectedItem()
        elif k == 27: #Escape key, exit with non zero code
            sys.exit(-1)
        elif isAlpha(k):
            m.addSearchCh(str(unichr(k)))

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def drive(menuItems):
    os.environ.setdefault('ESCDELAY', '25')
    return curses.wrapper(draw_menu, menuItems)
