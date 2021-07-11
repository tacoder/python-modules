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

class SshEditProcessor:
     def getMenuItems(self, typeOfMenu, context):
         conn = sqlite3.connect(SQLITE_DB)
         c = conn.cursor()
         dbEntries = c.execute('select * from ssh_hosts')
         sshHosts = [{"menuDesc":"New"}]
         sshHosts.extend([ menuItem(x[0],x[1],x[2],x[3]) for x in dbEntries])
         return  sshHosts
     def getThreshold(self, typeOfMenu, context):
         return 30
     def executeAction(self, choice):
         print("ssh-ing to server",choice["menuDesc"])
     def manipulateChoice(self, choice):
         if choice["menuDesc"] != "New":
             print("Update old config:: Leave blank to retain old values ")
             new_ip = raw_input('Enter ip [' + choice["ip"] + ']')
             new_username = raw_input('Enter username [' + choice["username"] + ']')
             new_nickname = raw_input('Enter nickname [' + choice["nickname"] + ']')
             if new_ip == "":
                 new_ip = choice["ip"]
             if new_username == "":
                 new_username = choice["username"]
             if new_nickname == "":
                 new_nickname = choice["nickname"]
             print("Testing echo command ssh to " , connString(new_username, new_ip))
             if subprocess.call(["ssh","-o","ConnectTimeout=10",connString(new_username, new_ip),"echo test"] ) != 0:
                  verification = raw_input('Connection failed, force input? (y/n): ')
                  confirm = verification.lower() in ['','y','yes','yee','ye','yeah']
                  if not confirm:
                      exit(1)
             conn = sqlite3.connect(SQLITE_DB)
             c = conn.cursor()
             c.execute("update ssh_hosts set  nickname=? , username=?, ip=? where id = ?",(new_nickname, new_username, new_ip, choice['id']))
             c.execute("delete from usage_log where config_type in ('ssh_edit', 'ssh') and value like '%" + menuDesc(choice["nickname"], choice["username"],choice["ip"]) + "%'")
             conn.commit()
             return menuItem(None , new_nickname, new_username, new_ip)
         print("Enter new config:: ")
         ip = raw_input('Enter ip: ')
         nickname = raw_input('Enter nickname (Leave blank for none): ')
         username = raw_input('Enter username (Leave blank for none): ')

         print("Testing echo command ssh to " , connString(username, ip))

         if subprocess.call(["ssh","-o", "ConnectTimeout=10",connString(username, ip),"echo test"]) != 0:
             verification = raw_input('Connection failed, force input? (y/n): ')
             confirm = verification.lower() in ['','y','yes','yee','ye','yeah']
             if not confirm:
                 exit(1)

         conn = sqlite3.connect(SQLITE_DB)
         c = conn.cursor()
         c.execute("insert into ssh_hosts (nickname, username, ip) values (?,?,?)",(nickname, username, ip))
         #print "Executing delete ","delete from usage_log where config_type in ('ssh_edit', 'ssh') and value like '%" + menuDesc(choice["username"],choice["ip"]) + "%'"
         #c.execute("delete from usage_log where config_type in ('ssh_edit', 'ssh') and value like '%" + menuDesc(choice["username"],choice["ip"]) + "%'")
         conn.commit()
         return menuItem(None, nickname, username, ip)
         #return {"menuDesc":ip + " - " + alias, "ip":ip,"alias":alias}
     def commandToRun(self, choice):
         return "ssh " + choice["ip"]
