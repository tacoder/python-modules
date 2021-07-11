from curses_modules.filtering_menu_driver import drive

def truncatedMenu(menuItems, threshold):
    truncatedMenuItems = menuItems[:threshold]
    if(len(menuItems)>threshold):
        truncatedMenuItems.append({"menuDesc":" .. More", "isMore":True})
    return truncatedMenuItems

def getChoiceFromMenu(menuItems, threshold):
    output = drive(truncatedMenu(menuItems, threshold))
    if "isMore" in output:
        output = drive(menuItems)
    return (output)

def main():
    getChoiceFromMenu([{"menuDesc":"first"},{"menuDesc":"first"},{"menuDesc":"first"}],3);

if __name__ == "__main__":
    main()
