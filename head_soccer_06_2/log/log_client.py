__author__ = 'grandt'
from PodSixNet.Connection import connection,ConnectionListener
import time

class LogClass(ConnectionListener):
    def __init__(self,ip = "localhost",port = 1998):
        self.ip,self.port = ip,port
        self.running = False
        if self.running:
            self.Connect((self.ip,self.port))
        self.connected = False
        self.retrying = {"Error at":time.time(),"Retrying":False}
        self.saved_basic = None
        self.saved_prints = []
    def Network_connected(self,data):
        print "Connected to server"
        self.connected = True
        if self.saved_basic:
            self.Send(self.saved_basic)
    def Network_disconnected(self,data):
        print "Disconnected from server, retrying in 5 seconds"
        self.connected = False
        self.retrying["Retrying"] = True
        self.retrying["Error at"] = time.time()
    def Network_error(self,data):
        #print data["error"][1],"Retrying in 5 seconds"
        self.retrying["Retrying"] = True
        self.retrying["Error at"] = time.time()
    def LogicUpdate(self):
        if self.running:
            ### Updating lib ###
            self.Pump()
            connection.Pump()
            ### Retrying connection ###
            if self.retrying["Retrying"]:
                if time.time() - self.retrying["Error at"] > 5:
                    self.retrying["Retrying"] = False
                    self.Connect((self.ip,self.port))
            if self.connected:
                if len(self.saved_prints) != 0:
                    for x in self.saved_prints:
                        self.Print(*x)
                        self.saved_prints = []
    def PrintError(self,*args):
        if self.running and self.connected:
            self.Send({"action":"print","print":args,"error":True})
        elif not self.connected:
            self.saved_prints.append(args)
        else:
            for x in args:
                print x,
            raise
    def Print(self,*args):
        if self.running and self.connected:
            self.Send({"action":"print","print":args,"error":False})
        elif not self.connected:
            self.saved_prints.append(args)
        else:
            for x in args:
                print x,
    def SetBasic(self,name,title_color,color,column):
        action = {"action":"set_basic","name":name,"title color":title_color,"color":color,"column":column}
        if self.connected:
            self.Send(action)
        else:
            self.saved_basic = action

Log = LogClass()