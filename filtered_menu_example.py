#!/usr/bin/python
import sys
from curses_modules.filtered_menu_driver import drive
import logging, logging.config

logger = logging.getLogger(__name__)


def main():
    if "-debug" in sys.argv:
        print "Enabling logs"
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
    menuItems = []
    for number in range(1,5):
        menuItems+=[{"menuDesc":"LONG NAME FOR AN ITEM item number" + str(number)}]
    output = drive(menuItems)
    print "user selected " + str(output)

if __name__ == "__main__":
    main()
