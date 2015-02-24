__author__ = 'Dylan'

import _mysql
import time

con = _mysql.connect('sql3.freemysqlhosting.net','sql368189','zL8!bB6%','sql368189') # Connecting to database

class SQLEngine:
    def CheckDeadServers(self):
        actual = self.GetServers()
        for x in actual:
            if int(x["Created"]) < int(time.time()) - 120:
                self.RemoveServer(x["IP"],x["Name"])
    def AddServer(self,name,ip):
        ### Add server to Servers database ###
        con.query("SELECT * FROM Servers WHERE Name = '"+name+"' AND IP = '"+ip+"'")
        if con.store_result().num_rows() == 0:
            con.query("INSERT INTO Servers (Name,IP,Created) VALUES ('"+name+"','"+ip+"',"+str(time.time())+")")
            return True
        else:
            return False
    def RemoveServer(self,ip,name):
        ### Remove server from Servers database by IP
        con.query("DELETE FROM Servers WHERE IP = '"+ip+"' AND Name = '"+name+"'")
    def GetServers(self):
        ### Return list of servers ###
        con.query("SELECT * FROM Servers")
        res = con.store_result()
        servers = []
        for x in range(res.num_rows()):
            data = list(res.fetch_row())[0]
            servers.append({"Name":data[0],"IP":data[1],"Created":data[2]})
        return servers
    def UpdateServer(self,ip,name):
        try:
            con.query("UPDATE Servers SET Created="+str(time.time())+" WHERE IP = '"+ip+"' AND Name = '"+name+"'")
        except:
            pass

MySQL = SQLEngine()