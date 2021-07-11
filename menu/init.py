import os
import sqlite3
import constants
from constants import SQLITE_DB

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

CREATE_SSH_HOSTS="""
create table if not exists ssh_hosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname varchar(256),
    username varchar(100),
    ip varchar(20)
)
"""

print("making file at ", SQLITE_DB)
conn = sqlite3.connect(SQLITE_DB)
c = conn.cursor()
c.execute(CREATE_USAGE_LOG)
#c.execute(CREATE_CONFIG)
c.execute(CREATE_SSH_HOSTS)
