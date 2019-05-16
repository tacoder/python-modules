#!/usr/bin/python
import sys
from curses_modules.filtering_menu_driver import drive
import logging, logging.config

logger = logging.getLogger(__name__)


def main():
    if "-debug" in sys.argv:
        print "Enabling logs"
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
    menuItems = []
    for number in ['master','telemetry-add-breakpoints','octref/58555','octref/panel-sidebar-focus','alexr00/clearTerminalBeforeTask','alexr00/TaskExitNotFiring','tyriar/electron-3.0.x-conpty','ben/ws-storage','electron-3.0.x','release/1.28','#60607 Merged','chrmarti/60243','chrmarti/51986','rebornix/nativeWordOperation','standalone/0.15.x','ramyar/copy-suggest-docs','joao/next','master','telemetry-add-breakpoints','octref/58555','octref/panel-sidebar-focus','alexr00/clearTerminalBeforeTask','alexr00/TaskExitNotFiring','tyriar/electron-3.0.x-conpty','ben/ws-storage','electron-3.0.x','release/1.28','#60607 Merged','chrmarti/60243','chrmarti/51986','rebornix/nativeWordOperation','standalone/0.15.x','ramyar/copy-suggest-docs','joao/next']:
        menuItems+=[{"menuDesc":str(number)}]
    output = drive(menuItems)
    print "user selected " + str(output)

if __name__ == "__main__":
    main()
