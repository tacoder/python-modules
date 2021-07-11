#!/usr/bin/python
import sys,os
import curses
from curses_modules.basic_menu import BasicMenu
import logging

logger = logging.getLogger(__name__)


def draw_menu(stdscr, menuItems):
    k=0
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    m = BasicMenu(stdscr,menuItems)
    m.render()

    # Loop where k is the last character pressed
    while (True):

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
        elif k == curses.KEY_ENTER or k == 10:
            logger.debug("Retunging.")
            return m.getCurrentlySelectedItem()
        elif k == 27: #Escape key, exit with non zero code
            sys.exit(-1)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def drive(menuItems):
    os.environ.setdefault('ESCDELAY', '25')
    return curses.wrapper(draw_menu, menuItems)