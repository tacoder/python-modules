import git
def removeOriginFromName(str):
    if str.startswith("origin/"):
        return str[7:]
    else:
        return str

class GitBranchProcessor:
     def getMenuItems(self, typeOfMenu, context):
         repo = git.Repo(context)
         return [ {"menuDesc":removeOriginFromName(x.name), "baseDir":context} for x in repo.refs ]
         #return  [{"menuDesc":"First"},{"menuDesc":"Second"},{"menuDesc":"Third"}]
     def getThreshold(self, typeOfMenu, context):
         return 30000
     def executeAction(self, choice):
         print("Switching to branch ",choice["menuDesc"])
     def commandToRun(self, choice):
         return "git checkout " + choice["menuDesc"]
