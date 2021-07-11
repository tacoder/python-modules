import argparse
from processors import factory
from sys import exit
from truncated_menu import getChoiceFromMenu
import usageManager
import logging
# from sets import Set

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='Generates a menu and takes action. Menu is populated on basis of context and type. It can be pre-filled or filled on usage. Sorting will be done basis some logic specific to type.')

parser.add_argument('--type', help='type of menu')
parser.add_argument('--context', required=False, default='',help='context of menu type')

args = parser.parse_args()

typeOfMenu = args.type
context = args.context
# print(args)

# To perform certain functions based on arguments given

def deduplicate(arr):
    #arr = [{'menuDesc': 'First'}, {'menuDesc': 'Second'}, {'menuDesc': 'Third'}, {'menuDesc': 'Second'}, {'menuDesc': 'Third'}]
    arr2 = []
    s = set()
    for entry in arr:
       if entry is None:
           continue
       name = entry['menuDesc']
       if name not in s:
         s.add(name)
         arr2.append(entry)
    return arr2

def merge(menuItems, recentItems):
    logger.debug("%s %s", menuItems, recentItems)
    mergedList = recentItems + menuItems
    return deduplicate(mergedList)

def writeCommandToFile(command):
    file = open("/tmp/menu_command.sh","w")
    file.write(command)
    file.close()

def main():
     if typeOfMenu not in factory:
         logger.error("Invalid type!")
         exit(1)
     else:
         processor = factory[typeOfMenu]
         logger.debug("generating menu for type: %s, context %s",typeOfMenu,context)
         menuItems = processor.getMenuItems(typeOfMenu, context)
         menuThreshold = processor.getThreshold(typeOfMenu, context)
         recentItems = usageManager.getRecentItems(typeOfMenu, context)
         menuItems = merge(menuItems, recentItems)
         logger.debug("%s",menuItems)
         choice = getChoiceFromMenu(menuItems, menuThreshold)
         try:
             choice = processor.manipulateChoice(choice)
         except AttributeError:
             pass
         usageManager.logUsage(typeOfMenu, choice, context)
         processor.executeAction(choice)
         commandToRun = processor.commandToRun(choice)
         writeCommandToFile(commandToRun)

if __name__ == "__main__":
    logging.info("Begin")
    main()

