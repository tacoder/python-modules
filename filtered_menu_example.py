#!/usr/bin/python
import sys,os
import curses
import json

from curses_modules.filtering_menu_inherited  import FilteringMenu
import curses


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

    for number in range(1,105):
        menuItems+=[{"menuDesc":"LONG ASS NAME FOR AN ITEM item number" + str(number)}]
    m = FilteringMenu(stdscr,menuItems)
    m.render()

#    m.increaseOffset()


    # Loop where k is the last character pressed
    while (k != ord('q')):

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

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    print "before"
    outptu = curses.wrapper(draw_menu)
    print outptu
    print "asdf"

if __name__ == "__main__":
    main()
