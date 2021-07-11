import os
import sqlite3
import constants
from constants import SQLITE_DB
import json
import subprocess

"""
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     nickname varchar(256),
     username varchar(100),
     ip varchar(20)
"""

def connString(username, ip):
     connString = ""
     if username is not None and username != "":
         connString += username + "@"
     connString+=ip
     return connString

def menuDesc(nickname, username, ip):
     menuDesc = nickname+" - "+connString(username, ip)
     return menuDesc

def menuItem(table_id, nickname, username, ip):
     return {"id":table_id,"menuDesc":menuDesc(nickname,username,ip),"nickname":nickname,"username":username,"ip":ip}

class SshProcessor:
     def getMenuItems(self, typeOfMenu, context):
           conn = sqlite3.connect(SQLITE_DB)
           c = conn.cursor()
           dbEntries = c.execute('select * from ssh_hosts')
           sshHosts = []
           sshHosts.extend([ menuItem(x[0],x[1],x[2],x[3]) for x in dbEntries])
           return  sshHosts
     def getThreshold(self, typeOfMenu, context):
         return 30000
     def executeAction(self, choice):
         print("ssh-ing to server",choice["menuDesc"])
     def commandToRun(self, choice):
         return "ssh " + connString(choice["username"],choice["ip"])
