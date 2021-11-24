# Should output 2 functions:
# getRecentItems(typeOfMenu, context)
# logUsage(typeOfMenu, choice, context)

import os
import sqlite3
import constants
from constants import SQLITE_DB
import json

CREATE_USAGE_LOG="""
create table if not exists usage_log (
    config_type varchar(50) not null,
    context varchar(1000) null,
    value varchar(1000),
    created timestamp default CURRENT_TIMESTAMP
);
"""

CREATE_CONFIG="""
create table if not exists config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    desc varchar(50)
)
"""

#conn = sqlite3.connect(SQLITE_DB)
#c = conn.cursor()
#c.execute(CREATE_USAGE_LOG)
#c.execute(CREATE_CONFIG)

def getRecentItems(typeOfMenu, context):
    conn = sqlite3.connect(SQLITE_DB)
    c = conn.cursor()
    dbEntries = c.execute('select distinct config_type, context, value from (select distinct config_type, context, value, created, sum(1/ (julianday(datetime(\'now\')) - julianday(created))) from usage_log where config_type=? and context=? and created > datetime(\'now\', \'-30 days\')  group by value order by 5 desc );',(typeOfMenu, context)).fetchall()
    #dbEntries = c.execute('select distinct config_type, context, value from usage_log where config_type=? and context=? order by created desc',(typeOfMenu, context)).fetchall()
    return [ json.loads(x[2]) for x in dbEntries ]
 #  return [{"menuDesc":"RecentFirst"},{"menuDesc":"RecnetSecond"},{"menuDesc":"RThird"}]

def logUsage(typeOfMenu, choice, context):
    conn = sqlite3.connect(SQLITE_DB)
    c = conn.cursor()
    c.execute("insert into usage_log (config_type, context, value) values (?,?,?)", (typeOfMenu, context, json.dumps(choice)))
    conn.commit()
