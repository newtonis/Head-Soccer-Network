__author__ = 'newtonis'
import sqlite3

def CheckOpinionNeed(ip):
    conn = sqlite3.connect("server_db/server.db")
    c = conn.cursor()
    for row in c.execute("SELECT * FROM opinion WHERE ip=:the_ip",{"the_ip":ip}):
        return False
    return True
    conn.commit()
    conn.close()

def AddOpinion(ip,question,opinion):
    conn = sqlite3.connect("server_db/server.db")
    c = conn.cursor()
    c.execute("INSERT INTO opinion (ip,question,option) VALUES (:the_ip,:the_question,:the_opinion)",({"the_ip":ip,"the_question":question,"the_opinion":opinion}))
    conn.commit()
    conn.close()

def CheckLogin(user,password):
    conn = sqlite3.connect("server_db/server.db")
    c = conn.cursor()
    res = c.execute("SELECT * FROM login WHERE Username = :the_user",{"the_user":user})
    ret = False
    error = "Username don't exists"
    for row in res:
        if row[2] == password:
            ret = True
        else:
            error = "Password don't match"
    conn.commit()
    conn.close()
    return {"Works":ret,"Error":error}

def AddUser(user,password,email):
    conn = sqlite3.connect("server_db/server.db")
    c = conn.cursor()
    res = c.execute("SELECT * FROM login")
    ID = 0
    ret = True
    for row in res:
        ID += 1
        if row[1] == user:
            ret = False
    if ret:
        c.execute("INSERT INTO login (ID,Username,Password,Email) VALUES (:id,:user,:pass,:email)",{"id":ID,"user":user,"pass":password,"email":email})
    conn.commit()
    conn.close()
    return ret

def DeleteUser(user,password):
    conn = sqlite3.connect("server_db/server.db")
    if CheckLogin(user,password)["Works"]:
        c = conn.cursor()
        c.execute("DELETE FROM login WHERE Username = :user",{"user":user})
        conn.commit()
        conn.close()

def DeleteTable(table):
    conn = sqlite3.connect("server_db/server.db")
    c = conn.cursor()
    c.execute("DROP TABLE :name",{"name":table})
    conn.commit()
    conn.close()