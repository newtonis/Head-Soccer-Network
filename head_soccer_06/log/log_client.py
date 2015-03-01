__author__ = 'grandt'
from PodSixNet.Connection import connection,ConnectionListener
import time

class Log(ConnectionListener):
    def __init__(self):
        self.ip,self.port = "localhost",9998
        self.Connect((self.ip,self.port))
        self.running = True
        self.connected = False
        self.retrying = {"Error at":time.time(),"Retrying":False}
    def Network_socketConnect(self,data):
        print "Connected to server"
        self.connected = True
    def Network_error(self,data):
        print data["error"][1],"Retrying in 5 seconds"
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
    def Print(self,*args):
        self.Send({"action":"print","print":args})
    def SetBasic(self,name,title_color,color):
        self.Send({"action":"set_basic","name":name,"title color":title_color,"color":color})

if __name__ == "__main__":
    log = Log()
    log.SetBasic("Server",(0,166,255),(0,226,255))
    log.Print("hola que tal como estas todo bien esto esta muy bien y es una prueba de que tal anda en multiple linea el algoritmo que hice para el texto")
    finished = False
    while not finished:
        log.LogicUpdate()