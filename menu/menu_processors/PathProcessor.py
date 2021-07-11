import os

class PathProcessor:
     def getMenuItems(self, typeOfMenu, context):
         subdirs=next(os.walk(context))[1]
         return [{"menuDesc":x, "root":context} for x in subdirs]
         #return  [{"menuDesc":"First"},{"menuDesc":"Second"},{"menuDesc":"Third"}]
     def getThreshold(self, typeOfMenu, context):
         return 30000
     def executeAction(self, choice):
         print("cd ",choice["root"] , "/" , choice["menuDesc"])
     def commandToRun(self, choice):
         return "cd " + choice["root"] + "/" + choice["menuDesc"]
