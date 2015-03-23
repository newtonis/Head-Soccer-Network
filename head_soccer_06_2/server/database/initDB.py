__author__ = 'newtonis'

import sqlite3
import pygame

def InitDB():
    conn = sqlite3.connect("server_db/server.db")
    c = conn.cursor()
    c.execute("CREATE TABLE opinion (ip TEXT,question int,option int)")
    conn.commit()
    conn.close()