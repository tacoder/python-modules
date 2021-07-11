from menu_processors.TestProcessor import TestProcessor
from menu_processors.PathProcessor import PathProcessor
from menu_processors.GitBranchProcessor import GitBranchProcessor
from menu_processors.SshProcessor import SshProcessor
from menu_processors.SshEditProcessor import SshEditProcessor
class TestProcessor:
    def getMenuItems(self, typeOfMenu, context):
        return  [{"menuDesc":"First"},{"menuDesc":"Second"},{"menuDesc":"Third"}]
    def getThreshold(self, typeOfMenu, context):
        return 2
    def executeAction(self, choice):
        print("You have chosen",choice)
"""
     menuItems = processor.getMenuItems(typeOfMenu, context)
     menuThreshold = processor.getThreshold(typeOfMenu, context)
     choice = getChoiceFromMenu(menuItems, menuThreshold)
     processor.executeAction(choice)
     """









factory={"test":TestProcessor(), "folder": PathProcessor(), "git_branch": GitBranchProcessor(), "ssh": SshProcessor(), "ssh_edit": SshEditProcessor()}
