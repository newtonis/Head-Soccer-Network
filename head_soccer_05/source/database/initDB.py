__author__ = 'newtonis'
import sqlite3

def InitDB():
    conn = sqlite3.connect("databases/servers.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE servers (ip TEXT,name TEXTS) ''')
    c.execute(''' INSERT INTO servers (ip,name) VALUES ('localhost','Local game') ''')
    c.execute(''' INSERT INTO servers (ip,name) VALUES ('192.168.1.1','Dylan server') ''')
    for row in c.execute("SELECT * FROM SERVERS"):
        print row
    conn.commit()
    conn.close()