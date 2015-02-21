__author__ = 'newtonis'

import sqlite3

def GetServerList():
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()

    data = []
    for row in c.execute("SELECT * FROM servers"):
        data.append(row)
    print "Server list obtained"
    conn.commit()
    conn.close()
    return data

def AddServer(server_name,server_ip):
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()

    c.execute("INSERT INTO servers VALUES (?,?)",(server_name,server_ip))
    conn.commit()
    conn.close()
    print "Server added to db"

def UpdateServer(server_name,ip):
    print "Changing",server_name,"ip to",ip
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=:the_ip WHERE name=:the_server_name",{"the_ip":ip,"the_server_name":server_name})

    conn.commit()
    conn.close()

def DeleteServer(server_name):
    print "Deleting server",server_name
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()
    c.execute("DELETE FROM servers WHERE name=:the_server_name",{"the_server_name":server_name})

    conn.commit()
    conn.close()

def UpdateTresHold(value):
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()
    c.execute("UPDATE config SET threshold=:th",{"th":value})
    conn.commit()
    conn.close()

def UpdateInterpolation(value):
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()
    c.execute("UPDATE config SET interpolation=:int",{"int":value})
    conn.commit()
    conn.close()

def UpdateConfig(threshold,interpolation):
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()
    c.execute("UPDATE config SET threshold=:th,interpolation=:int",{"th":threshold,"int":interpolation})
    conn.commit()
    conn.close()

def GetConfigData():
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()

    for row in c.execute("SELECT * FROM config"):
        data = row

    conn.commit()
    conn.close()

    return data