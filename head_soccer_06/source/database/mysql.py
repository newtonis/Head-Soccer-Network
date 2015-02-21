__author__ = 'Dylan'

import _mysql

global con
con = _mysql.connect('sql3.freemysqlhosting.net','sql368189','zL8!bB6%','sql368189') # Connecting to database

def CreateTable(name,columns):
    """
    :param name:    Table name
    :param columns: Array of dicts with column data
    :return:        Return mysql return
    """
    text = "CREATE TABLE "+str(name)+" IF NOT EXISTS "
    for column in columns:
        text += "("+column["name"]+" "

    con.query(text)