__author__ = 'newtonis'
import sqlite3

def CheckOpinionNeed(ip):
    conn = sqlite3.connect("server_db/opinion.db")
    c = conn.cursor()
    for row in c.execute("SELECT * FROM opinion WHERE ip=:the_ip",{"the_ip":ip}):
        return False
    return True
    conn.commit()
    conn.close()

def AddOpinion(ip,question,opinion):
    conn = sqlite3.connect("server_db/opinion.db")
    c = conn.cursor()
    c.execute("INSERT INTO opinion (ip,question,option) VALUES (:the_ip,:the_question,:the_opinion)",({"the_ip":ip,"the_question":question,"the_opinion":opinion}))
    conn.commit()
    conn.close()