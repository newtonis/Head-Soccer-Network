__author__ = 'newtonis'
import sqlite3

def InitDB():
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE servers (ip TEXT,name TEXT) ''')
    c.execute(''' INSERT INTO servers (ip,name) VALUES ('localhost','Local game') ''')
    c.execute(''' INSERT INTO servers (ip,name) VALUES ('192.168.1.1','Dylan server') ''')
    for row in c.execute("SELECT * FROM SERVERS"):
        print row
    conn.commit()
    conn.close()

def initConfigDB():
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE config (interpolation REAL,threshold REAL) ''')
    c.execute('''INSERT INTO config (interpolation,threshold) VALUES (0.3,0.001)''')

    conn.commit()
    conn.close()
