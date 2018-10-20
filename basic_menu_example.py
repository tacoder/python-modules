#!/usr/bin/python
import sys
from curses_modules.basic_menu_driver import drive

def main():
    if "-debug" in sys.argv:
        print "Enabling logs"
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
    menuItems = []
    for number in range(1,100):
        menuItems+=[{"menuDesc":"LONG NAME FOR AN ITEM item number" + str(number)}]
    output = drive(menuItems)
    print "user selected " + str(output)


if __name__ == "__main__":
    main()
