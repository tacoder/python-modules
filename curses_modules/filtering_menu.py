#!/usr/bin/python
import sys,os
import curses
import json
from basic_menu import BasicMenu

stdscrObj = None
import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/var/tmp/myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

'''
FIltering menu:

should render a search bar at bottom.

Should provide 2 function additionally:

add search char
remove search char

both need to perform below functions:
add/remove from buffered search string
filter in/out eligible menu items
redraw menu if needed - 
## Keeping this functionality in pipeline -- keep selected item selected if it is not filtered out.

'''
class FilteringMenu(BasicMenu):
    def __init__(self, winObj, menuItems, menuBackgroundColor=curses.COLOR_BLACK, menuForegroundColor=curses.COLOR_WHITE, borderBackgroundColor=curses.COLOR_BLACK, borderForegroundColor=curses.COLOR_WHITE, leftPadding=2, scrollPadding=None):
        BasicMenu.__init__(self,winObj, menuItems, menuBackgroundColor, menuForegroundColor, borderBackgroundColor, borderForegroundColor, leftPadding, scrollPadding)
        self.menuEnd = self.height - 2 - 3
        self.menuHeight = self.menuEnd - self.menuStart + 1
                # Set default scroll padding, if needed:
        if(scrollPadding is None):
            self.scrollPadding = int(self.menuHeight*0.15)
        # Restrict scroll padding -
        if(self.scrollPadding > (self.height / 2)):
            self.scrollPadding = self.height / 2


    def drawBorder(self):
        BasicMenu.drawBorder(self)
        self.window.border()
        self.window.addch(self.height-4,0,curses.ACS_LTEE)
        for i in range (1, self.width-1):
            self.window.addch(self.height-4,i,curses.ACS_HLINE)
        self.window.addch(self.height-4,self.width-1,curses.ACS_RTEE)


