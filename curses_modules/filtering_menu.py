#!/usr/bin/python
import sys,os
import curses
import json

stdscrObj = None
import logging
logger = logging.getLogger(__name__)
# hdlr = logging.FileHandler('/var/tmp/myapp.log')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.DEBUG)

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
class FilteringMenu():
    def __init__(self, winObj, menuItems, menuBackgroundColor=curses.COLOR_BLACK, menuForegroundColor=curses.COLOR_WHITE, borderBackgroundColor=curses.COLOR_BLACK, borderForegroundColor=curses.COLOR_WHITE, leftPadding=2, scrollPadding=None):

        # Set design properties
        self.menuBGcolor = menuBackgroundColor
        self.menuFGcolor = menuForegroundColor
        self.borderBGcolor = borderBackgroundColor
        self.borderFGcolor = borderForegroundColor
        self.leftPadding = leftPadding
        self.scrollPadding = scrollPadding

        # Set menu static properties -- those that will not change generally
        self.window = winObj
        self.originalMenuItems = menuItems
        self.inputMenuItems = menuItems
        self.height, self.width = self.window.getmaxyx()
        self.menuStart = 1  
        self.menuEnd = self.height - 2 - 2
        self.menuHeight = self.menuEnd - self.menuStart + 1
        self.size = len(menuItems)
        self.firstItem = 0
        self.lastItem = self.firstItem + self.size - 1
        self.menuItemWidth = self.width - 2 - self.leftPadding

        # set dynamic properties - these will change regularly, and contain
        self.offset = 0
        self.currentlySelectedItemIndex = 0
        self.initDefaultColors()

        # Set default scroll padding, if needed:
        if(scrollPadding is None):
            self.scrollPadding = int(self.menuHeight*0.15)
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

        self.searchBarPos = self.height - 2 - 0
        self.searchStr = ""

    def drawBorder(self):
        self.window.border()
        self.window.addch(self.height-3,0,curses.ACS_LTEE)
        for i in range (1, self.width-1):
            self.window.addch(self.height-3,i,curses.ACS_HLINE)
        self.window.addch(self.height-3,self.width-1,curses.ACS_RTEE)

    def addSearchCh(self, searchCh):
        logger.debug("event: addding search ch " + str(searchCh))
        self.searchStr += searchCh
        logger.debug("New search string is" + self.searchStr)
        self.addCh(searchCh)

    def removeSearchCh(self):
        logger.debug("event: removing search ch")
        if(len(self.searchStr)>0):
            self.searchStr = self.searchStr[:-1]
            self.removeCh()

    def filterAndRedraw(self):
        filteredMenuItems = []
        for menuItem in self.originalMenuItems:
            logger.debug("Attempting to match " + str(menuItem) + " with " + str(self.searchStr))
            if self.searchStr.lower() in menuItem["menuDesc"].lower():
                logger.debug("Filtering menu item " + str(menuItem));
                filteredMenuItems.append(menuItem)
        logger.debug("filtered items are " + str(filteredMenuItems))
        self.inputMenuItems = filteredMenuItems
        self.offset = 0
        self.size = len(filteredMenuItems)
        self.lastItem = self.firstItem + self.size - 1
        self.render()


    def addCh(self, searchCh):
        self.window.addch(self.searchBarPos, self.leftPadding + len(self.searchStr) - 1, searchCh)
        self.filterAndRedraw()

    def removeCh(self):
        self.window.addch(self.searchBarPos, self.leftPadding + len(self.searchStr) , " ")
        self.filterAndRedraw()


    def getDetails(self):
        return         "self.offset = " + str(self.offset) + ", "
        "self.currentlySelectedItemIndex = " + str(self.currentlySelectedItemIndex);


    def initDefaultColors(self):
        self.unselected = 0
        self.selected = 10
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # def __init__(self, winObj, menuItems):
    #     self.__init__(self, winObj, menuItems, None, None, None, None, None, None)
 
    def renderMenu(self):
        logger.debug("Rendering menu from " +str(0 + self.offset) + " to " + str(self.menuEnd + self.offset))
        for index in range (0 + self.offset, self.menuEnd + self.offset):
            # logger.debug("for loop " + str(index))
            if(index > self.lastItem or index < self.firstItem):
                self.window.addstr(index + self.menuStart - self.offset, self.leftPadding, self.justifyAndTrim("~"))
            else:    
                menuItem = self.inputMenuItems[index]
                self.window.addstr(index + self.menuStart - self.offset, self.leftPadding, self.justifyAndTrim(menuItem["menuDesc"]))

    def render(self):
        self.drawBorder()
        self.renderMenu()
        if(self.size > 0):
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
            if(itemToSelect < self.scrollPadding):
                self.offset = 0

        # Below currently selected object
        if(( renderPositionNew > (self.menuEnd - self.scrollPadding) ) and self.offset < self.size - self.menuHeight):
            needToAdjust = True
            self.offset = itemToSelect + self.scrollPadding - self.menuHeight

        return needToAdjust

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
        self.window.addstr(itemNoToColor + self.menuStart - self.offset, self.leftPadding, self.justifyAndTrim(self.inputMenuItems[itemNoToColor]["menuDesc"]))
        self.window.attroff(curses.color_pair(colorPairToApply))

    def down(self):
        logger.debug("event: DOWN")
        logger.debug("last item is " + str(self.lastItem))
        if( self.currentlySelectedItemIndex < self.lastItem ):
            self.selectItem(self.currentlySelectedItemIndex + 1)

    def up(self):
        logger.debug("event: UP")
        if( self.currentlySelectedItemIndex > self.firstItem ):
            self.selectItem(self.currentlySelectedItemIndex - 1)

    def justifyAndTrim(self, str):
        return str.ljust(self.menuItemWidth)[:self.menuItemWidth]

    def pagedown(self):
        logger.debug("event: PAGEDOWN")
        if( self.currentlySelectedItemIndex != self.lastItem ):
            newItem = self.currentlySelectedItemIndex + self.menuHeight
            if(newItem > self.lastItem):
                newItem = self.lastItem
            self.selectItem(newItem)

    def pageup(self):
        logger.debug("event: PAGEUP")
        if( self.currentlySelectedItemIndex != self.firstItem ):
            newItem = self.currentlySelectedItemIndex - self.menuHeight
            if(newItem < self.firstItem):
                newItem = self.firstItem
            self.selectItem(newItem)

    def getCurrentlySelectedItem(self):
        return self.inputMenuItems[self.currentlySelectedItemIndex]