__author__ = 'ariel'

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.ServerUDP import ServerUDP
import game_gg
import threading

class ServerChannel(Channel):
    def __init__(self , *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
	self.id = str(self._server.NextId())
        intid = int(self.id)
        self.name    = "Player " + str(self.id)
        self.events  = {"up":0,"left":0,"right":0}
        self.updateT = 40
        self.area    = "lobby" 

class Room(game_gg.Game):
    def __init__(self,id,name,type):
        self.id   = id
        self.name = name
        self.type = type
        self.game = game.Game()
    def GetData(self):
        return {"id":self.id,"name":self.name,"type":self.type}

class WhiteboardServer(Server):
    channelClass = ServerChannel
    def __init__(self,*args,**kwargs):
        self.playing = True
        self.log = []
        self.showLog = True
        self.AddLog("Starting server ...")
        self.id = 0
        self.player  = dict()
	self.rooms   = dict()
        Server.__init__(self,*args,**kwargs)
    def AddLog(self,log):
        if self.showLog:
            print ""
            print "Info:",log
            if self.playing:
                print ">>>",
        self.log.append(log)
    def NextId(self):
        self.id += 1
        return self.id
    def Connected(self , channel , addr):
        self.AddLog("Player connected ("+str(addr)+")")
        channel.Send({"action":"initial" , "type":"friendly_server", "content":self.GetRoomsInfo()})
        self.players[channel.id] = channel
        self.SendMessage("Welcome to friendly server",channel.id)
    def GetRoomsInfo(self):
        pass
    def SendMessage(self,message,playerID):
        self.players[playerID].Send({"action":"message","content":message})
    def SendMessageToAll(self,message):
        for pk in self.players.keys():
            self.SendMessage(message,pk)
    def Loop(self):
        self.Pump()
    def CommandsLoop(self):
        while self.playing:
            command = raw_input("")
            self.AnalizeCommand(command)    
            if self.playing:
                print ">>>",
    def AnalizeCommand(self,command):
        if command == "exit":
            self.CloseServer()
    def CloseServer(self):
        self.playing = False
        self.AddLog("Quiting server")
    def GetRoomsInfo(self):
        data = dict()
        for rk in self.rooms.keys():
            data[rk] = self.rooms[rk].GetData()
        return data

def main():
    server = WhiteboardServer(localaddr=("localhost",9999))
    threadCommands = threading.Thread(target=server.CommandsLoop)
    threadCommands.start()
    while server.playing:
        server.Loop()


if __name__ == "__main__":
     main()

