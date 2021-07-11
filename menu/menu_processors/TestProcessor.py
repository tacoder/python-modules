class TestProcessor:
     def getMenuItems(self, typeOfMenu, context):
         return  [{"menuDesc":"First"},{"menuDesc":"Second"},{"menuDesc":"Third"}]
     def getThreshold(self, typeOfMenu, context):
         return 2
     def executeAction(self, choice):
         print("You have chosen",choice)
