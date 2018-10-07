#!/usr/bin/python
import sys,os
import curses

stdscrObj = None

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
update default scroll padding to adjust with the height of menu.
Set static variables.
Implement said methods
'''

class menu:

    def initDefaultColors(self):
        self.unselected = 0
        self.selected = 10
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # def __init__(self, winObj, menuItems):
    #     self.__init__(self, winObj, menuItems, None, None, None, None, None, None)

    def __init__(self, winObj, menuItems, menuBackgroundColor=curses.COLOR_BLACK, menuForegroundColor=curses.COLOR_WHITE, borderBackgroundColor=curses.COLOR_BLACK, borderForegroundColor=curses.COLOR_WHITE, leftPadding=2, scrollPadding=10):

        # Set design properties
        self.design = {}
        self.design['color'] = {}
        self.design['color']['menu'] = {}
        self.design['color']['menu']['bg'] = menuBackgroundColor
        self.design['color']['menu']['fg'] = menuForegroundColor
        self.design['color']['border'] = {}
        self.design['color']['border']['bg'] = borderBackgroundColor
        self.design['color']['border']['fg'] = borderForegroundColor
        self.design['leftPadding'] = leftPadding
        self.design['scrollPadding'] = scrollPadding


        self.window = winObj
        self.menuItems = menuItems
        self.height, self.width = self.window.getmaxyx()
        self.offset = 0
        self.padding = 5
        self.menuStart = 1
        self.menuEnd = self.height - 2
        self.selectedItem = 0
        self.size = len(menuItems)
        self.LEFT_PAD = 2
        self.initDefaultColors()

    def drawBorder(self):
        self.window.border()

    def renderMenu(self):
        for index in range (0 + self.offset, self.menuEnd + self.offset):
#        for index, menuItem in enumerate(self.menuItems):
#            if(index >= self.menuEnd):
#                break
            menuItem = self.menuItems[index]
            self.window.addstr(index + self.menuStart - self.offset, self.LEFT_PAD, menuItem["menuDesc"])

    def render(self):
        self.drawBorder()
        self.renderMenu()
        self.selectItem(0)

    def selectItem(self, currentItemNo, previousItemNo=None):
        self.selectedItem = currentItemNo
        if previousItemNo is not None:
            self.colorItem(previousItemNo, self.unselected)
        self.colorItem(currentItemNo, self.selected)

    def colorItem(self, itemNoToColor, colorPairToApply):
        self.window.attron(curses.color_pair(colorPairToApply))
        self.window.addstr(itemNoToColor + self.menuStart - self.offset, self.LEFT_PAD, self.menuItems[itemNoToColor]["menuDesc"])
        self.window.attroff(curses.color_pair(colorPairToApply))

    def increaseOffset(self):
        self.offset = self.offset+1
        self.renderMenu()

    def down(self):
        if(self.selectedItem - self.offset > self.height -4):
            self.increaseOffset()
        if(self.selectedItem < self.size-1):
            self.selectItem(self.selectedItem + 1, self.selectedItem)

    def decreaseOffset(self):
        self.offset = self.offset-1
        self.renderMenu()

    def up(self):
        if(self.selectedItem > self.offset):
            self.decreaseOffset()
        if(self.selectedItem > 0):
            self.selectItem(self.selectedItem - 1, self.selectedItem)



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
    main()