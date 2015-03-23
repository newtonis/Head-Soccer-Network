__author__ = 'newtonis'
import sqlite3

#### This file contains the functions to access session db ####

def initSessionDB():
    conn = sqlite3.connect("databases/session.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE session (status REAL,server TEXT ,logtype REAL,username TEXT,password TEXT,room TEXT)''')
    c.execute("INSERT INTO session (status,server,logtype,username,password,room) values (0,'',0,'','',0) ")
    conn.commit()
    conn.close()
def SessionDeclareConnect(ip):
    conn = sqlite3.connect("databases/session.db")
    c = conn.cursor()
    c.execute("UPDATE session SET status=1,server=:the_ip,username='',password='',room=0",{"the_ip":ip})
    conn.commit()
    conn.close()
def SessionDeclareGuestName(name):
    print "logged as guest '",name,"'"
    conn = sqlite3.connect("databases/session.db")
    c = conn.cursor()
    c.execute("UPDATE session SET logtype=1,username=:the_name",{"the_name":name})
    conn.commit()
    conn.close()
def SessionDeclareLogin(user,password):
    print "logged as '",user,"' with pass '",password,"'"
    conn = sqlite3.connect("databases/session.db")
    c = conn.cursor()
    c.execute("UPDATE session SET logtype=2,username=:the_username,password=:the_password",{"the_username":user,"the_password":password})
    conn.commit()
    conn.close()
def SessionDeclareEnterRoom(room_id):
    conn = sqlite3.connect("databases/session.db")
    c = conn.cursor()
    c.execute("UPDATE session SET status=2,room=:the_room",{"the_room":room_id})
    conn.commit()
    conn.close()
def SessionDeclareExitRoom():
    conn = sqlite3.connect("databases/session.db")
    c = conn.cursor()
    c.execute("UPDATE session SET status=1")
    conn.commit()
    conn.close()
def SessionDeclareDisconnect():
    conn = sqlite3.connect("databases/session.db")
    c = conn.cursor()
    c.execute("UPDATE session SET status=0")
    conn.commit()
    conn.close()
def GetLoginData(data):
    if data[2] == 1: ## guest mode
        return {"type":"guest","name":data[3]}
    elif data[2] == 2: ##login mode
        return {"type":"login","name":data[3],"pass":data[4]}
    else:
        return {"type":"needGuestName"}
def GetSessionData():
    conn = sqlite3.connect("databases/session.db")
    c = conn.cursor()
    for row in c.execute("SELECT * FROM session"):
        data = row

    status = data[0]
    if status == 0:
        return {"status":"NoConnect"}
    if status == 1:
        return {"status":"TryConnect","ip":data[1],"logData":GetLoginData(data)}
    if status == 2:
        return {"status":"TryConnectRoom","ip":data[1],"logData":GetLoginData(data),"room":data[5]}

def standards(data):
    if data["status"] == "NoConnect":
        return 0
    if data["logData"]["type"] == "needGuestName":
        return 0
    return 1