#!/usr/bin/python
import sys,os
import curses
import json

stdscrObj = None

import logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/var/tmp/myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)
'''
menu

design attributes:
    colors - default B&W
    left padding - default 1
    scroll padding - default 10% of menu height

dimentions:
    height
    width

state attributes:
    currently highlighted
    menu render offset

functions to support:
    highlight item no i
    move up
    move down
'''


'''
TODO:
figure out default colors mapping! -- can we possibly move colors out of this class ? maybe, maybe not.
Implement said methods
'''

class menu:
    def getDetails(self):
        return         "self.offset = " + str(self.offset) + ", "
        "self.currentlySelectedItemIndex = " + str(self.currentlySelectedItemIndex);


    def initDefaultColors(self):
        self.unselected = 0
        self.selected = 10
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # def __init__(self, winObj, menuItems):
    #     self.__init__(self, winObj, menuItems, None, None, None, None, None, None)

    def __init__(self, winObj, menuItems, menuBackgroundColor=curses.COLOR_BLACK, menuForegroundColor=curses.COLOR_WHITE, borderBackgroundColor=curses.COLOR_BLACK, borderForegroundColor=curses.COLOR_WHITE, leftPadding=2, scrollPadding=10):

        # Set design properties
        self.menuBGcolor = menuBackgroundColor
        self.menuFGcolor = menuForegroundColor
        self.borderBGcolor = borderBackgroundColor
        self.borderFGcolor = borderForegroundColor
        self.leftPadding = leftPadding
        self.scrollPadding = scrollPadding

        # Set menu static properties -- those that will not change generally        
        self.window = winObj
        self.inputMenuItems = menuItems
        self.height, self.width = self.window.getmaxyx()
        self.menuStart = 1
        self.menuEnd = self.height - 2
        self.menuHeight = self.menuEnd - self.menuStart + 1
        self.size = len(menuItems)
        self.firstItem = 0
        self.lastItem = self.firstItem + self.size

        # set dynamic properties - these will change regularly, and contain
        self.offset = 0        
        self.currentlySelectedItemIndex = 0
        self.initDefaultColors()

        # Restrict scroll padding - 
        if(self.scrollPadding > (self.height / 2)):
            self.scrollPadding = self.height / 2

        logger.debug("Initialized menu with params : " +    "self.menuBGcolor = " + str(self.menuBGcolor) + ", " + 
        "self.menuFGcolor = " + str(self.menuFGcolor) + ", " + 
        "self.borderBGcolor = " + str(self.borderBGcolor) + ", " + 
        "self.borderFGcolor = " + str(self.borderFGcolor) + ", " + 
        "self.leftPadding = " + str(self.leftPadding) + ", " + 
        "self.scrollPadding = " + str(self.scrollPadding) + ", " + 
        "self.window = " + str(self.window) + ", " + 
        "self.inputMenuItems = " + str(self.inputMenuItems) + ", " + 
        "self.height = " + str(self.height) + ", " + 
        "self.menuStart = " + str(self.menuStart) + ", " + 
        "self.menuEnd = " + str(self.menuEnd) + ", " + 
        "self.menuHeight = " + str(self.menuHeight) + ", " + 
        "self.size = " + str(self.size) + ", " + 
        "self.firstItem = " + str(self.firstItem) + ", " + 
        "self.lastItem = " + str(self.lastItem) + ", ");

    def drawBorder(self):
        self.window.border()

    def renderMenu(self):
        for index in range (0 + self.offset, self.menuEnd + self.offset):
            menuItem = self.inputMenuItems[index]
            self.window.addstr(index + self.menuStart - self.offset, self.leftPadding, menuItem["menuDesc"])

    def render(self):
        self.drawBorder()
        self.renderMenu()
        self.selectItem(0)

    def renderPositionOf(self,itemToSelect):
        return itemToSelect - self.offset

    def adjustOffsetIfNeeded(self, itemToSelect):
        renderPositionNew = self.renderPositionOf(itemToSelect);
        needToAdjust = False
        # If menu item to be selected is beyond permissible render bounds 

        # Above currently selected object
        if(( renderPositionNew < (self.menuStart + self.scrollPadding) ) and self.offset > 0):
            needToAdjust = True
            self.offset = itemToSelect - self.scrollPadding
        
        # Below currently selected object
        if(( renderPositionNew > (self.menuEnd - self.scrollPadding) ) and self.offset < self.size - self.menuHeight):
            needToAdjust = True
            self.offset = itemToSelect + self.scrollPadding - self.size

        return needToAdjust
        # needToAdjust =  || (renderPositionNew > (self.menuEnd - self.scrollPadding))
        # if(needToAdjust):
        #     topRenderPosition = 
        #     bottomRenderPosition = 

    def selectItem(self, itemToSelect):
        logger.debug("Selecting item : " + str(itemToSelect))
        assert itemToSelect >= self.firstItem
        assert itemToSelect <= self.lastItem

        previousItemIndex = self.currentlySelectedItemIndex
        self.currentlySelectedItemIndex = itemToSelect
        isOffsetAdjust = self.adjustOffsetIfNeeded(itemToSelect);

        # Need to render entire menu in case offset is adjusted
        if(isOffsetAdjust):
            logger.debug("Adjusted offset. : " + self.getDetails())
            self.renderMenu()
        # Delect previous item if offset was not adjusted.
        else:
            if previousItemIndex is not None:
                self.colorItem(previousItemIndex, self.unselected)
        self.colorItem(itemToSelect, self.selected)

    def colorItem(self, itemNoToColor, colorPairToApply):
        self.window.attron(curses.color_pair(colorPairToApply))
        self.window.addstr(itemNoToColor + self.menuStart - self.offset, self.leftPadding, self.inputMenuItems[itemNoToColor]["menuDesc"])
        self.window.attroff(curses.color_pair(colorPairToApply))

    # def increaseOffset(self):
    #     self.offset = self.offset+1
    #     self.renderMenu()

    def down(self):
        logger.debug("event: DOWN")

        # if(self.currentlySelectedItemIndex - self.offset > self.height -4):
        #     self.increaseOffset()
        # if(self.currentlySelectedItemIndex < self.size-1):
        if( self.currentlySelectedItemIndex != self.lastItem ):
            self.selectItem(self.currentlySelectedItemIndex + 1)

    # def decreaseOffset(self):
    #     self.offset = self.offset-1
    #     self.renderMenu()

    def up(self):
        logger.debug("event: UP")
        if( self.currentlySelectedItemIndex != self.firstItem ):
            self.selectItem(self.currentlySelectedItemIndex - 1)



def draw_menu(stdscr):
    global stdscrObj
    stdscrObj = stdscr
    k = 0
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

    for number in range(1,100):
        menuItems+=[{"menuDesc":"item number" + str(number)}]
    m = menu(stdscr,menuItems)
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
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
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
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    logger.debug("Entering main!")
    main()
