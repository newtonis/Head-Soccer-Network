__author__ = 'newtonis'

import threading
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.ServerUDP import ServerUDP
from source.gui.getCenter import GetCenter
from game import *
from database import serverQ
import opinion
from source.data.images import Heads
from source.data import config
import random
from database.mysql import MySQL
import time
from log.log_client import Log

class ServerChannel(Channel):
    def __init__(self , *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())
        self.status = "checkData"
        self.ip = "nn"
        self.conn = "nn"
        self.name = "noName"
        self.guest = False
        self.head = Heads.heads[random.randrange(len(Heads.heads))]

        self.RoomDef = None
        #### UDP ####
        self.udpAddr = -1

        ### NEXT CC, FOR PING CALCULATOR
        self.nextCC = False
    #### UDP def ###
    def SendUDP(self,data):
        #print data,"sent in udp",self.udpAddr
        if self.udpAddr != -1:
            self._server.UDPconnector.Send(data,self.udpAddr)
    def Close(self):
        Log.Print("Player",self.GetID(),"has left the game")
        if config.CLOSE_WHEN_CLIENT_LOST:
            self._server.Close()
        if self.RoomDef:
            self.RoomDef(self,"lost")
        self._server.HandlePlayerLost(self)
    def Network_request_basic(self,data):
        Log.Print("Player",self.GetID(),"has decided to request basic information")
        self.SendBasic()
    def Network_request_basicUDP(self,data):
        Log.Print("request basic udp")
        self.SendBasicUDP()
    def Network_request_rooms(self,data):
        if self.status == "checkData":
            """print "Player",self.GetID()," has decided to join the game"
            allow , reason = self._server.AllowEntrance()
            if allow:
                if serverQ.CheckOpinionNeed(self.ip):
                    print "Opinion survey sent to player"
                    self.SendOpinion()
                else:
                    self.SendSkip()
                    print "No opinion survey needed"
                    print "Sending name request"
                    self.SendRequestName()

                    #self.SendRooms()
            else:
                print "However the server is full so the player will be rejected"
                self.SendNotAllow(reason)"""
            self.SendRequestName()
        elif self.status == "already-connected":
            Log.Print("Player",self.GetID(),"requested rooms again")
            self.SendRooms()
    def Network_get_opinion(self,data):
        Log.Print("Player",self.GetID(),"opinion has arrived")
        if data["option"] >= len(self.opinion["options"]):
            Log.Print("Opinion corrupted!",data["option"])
        else:
            Log.Print(self.opinion["question"])
            Log.Print("He has elected '"+self.opinion["options"][data["option"]]+"'")
            serverQ.AddOpinion(self.ip,self.opinion["id"],data["option"])
        self.SendRequestName()
    def Network_send_name(self,data):
        allowed_name = True
        error = ""
        for x in self._server.clients.keys():
            if self._server.clients[x].name == data["name"]:
                allowed_name = False
                error = "Name already in use"
        if len(data["name"]) < 4:
            allowed_name = False
            error  = "Name too short"
        if allowed_name:
            self.name = data["name"]
            self.guest = True
            self.SendRooms()
        else:
            self.Send({"action":"name_error","error":error})
    def Network_join_game(self,data):
        Log.Print("Player",self.GetID(),"want to join to room",data["room_name"])
        self._server.JoinPlayer(self,data["room_name"])
    def Network_exit_game(self,data):
        self.RoomDef(self,"exit",data)
    def Network_req_av_players(self,data):
        Log.Print("Player",self.GetID(),"requested players available")
        self.Send({"action":"data_players","players":self._server.GetPlayers(),"player-name":self.name})
    def Network_set_configuration(self,data):
        error = ""
        if data["name"] != None:
            for x in self._server.clients.keys():
                if self._server.clients[x].name == data["name"]:
                    error = "Name already in use"
            if len(data["name"]) < 4:
                error = "Name too short"
        else:
            data["name"] = self.name
        if error == "":
            Log.Print("Player",self.GetID(),"has just changed his/her name to",data["name"])
            self.name = data["name"]
        self.head = data["headcode"]
        self.Send({"action":"profile_conf_error","error":error})
    def Network_joinA(self,data):
        self.RoomDef(self,"joinA",data)
    def Network_joinB(self,data):
        self.RoomDef(self,"joinB",data)
    def Network_spectate(self,data):
        self.RoomDef(self,"spectate",data)
    def Network_keys(self,data):
        self.RoomDef(self,"keys",data)
    def Network_update_pos(self,data):
        self.RoomDef(self,"update_pos",data)
    def Network_send_chat(self,data):
        if self.RoomDef:
            self.RoomDef(self,"chat",{"From":self.name,"Message":data["message"]})
    def Network_bc(self,data):
        self.RoomDef(self,"bc",data)
    def Network_check_login(self,data):
        check = serverQ.CheckLogin(data["username"],data["password"])
        if check["Works"]:
            self.guest = False
            self.name = data["username"]
            self.Send({"action":"confirm_login","pass":"DT"})
            self.SendRooms()
        else:
            self.Send({"action":"confirm_login","pass":"error","error":check["Error"]})
    def Network_register(self,data):
        have_error = False
        error = ""
        if data["confirmation"] == data["password"]:
            register = serverQ.AddUser(data["username"],data["password"],data["email"])
            if register:
                pass
            else:
                error = "Username already exists"
        else:
            error = "Passwords don't match"
        self.Send({"action":"confirm_signup","error":error})
    def SetRoomDef(self,func):
        Log.Print("room def set")
        self.RoomDef = func
    def SendBasic(self):
        self.Send({"action":"basic_data","info":self._server.GetBasicInfo(),"id":self.id})
    def SendBasicUDP(self):
        self.SendUDP({"action":"udp_signal"})
    def SendRooms(self):
        self.status = "already-connected"
        self.Send({"action":"rooms_data","info":self._server.GetRoomsData()})
    def SendNotAllow(self,reason):
        self.Send({"action":"not_allowed","reason":reason})
    def SendOpinion(self):
        self.opinion = opinion.Random()
        self.Send({"action":"opinion","content":self.opinion})
    def SendSkip(self):
        self.Send({"action":"skip_opinion"})
    def SendRequestName(self):
        self.Send({"action":"request_name"})
    def GetID(self):
        if self.name != "noName":
            return "'"+str(self.name)+"'"
        else:
            return self.id
    def NextCC(self):
        self.nextCC = True
    def GetCC(self):
        if self.nextCC:
            self.nextCC = False
            return 1
        return 0

class WhiteboardServer(Server):
    channelClass = ServerChannel
    def __init__(self,*args,**kwargs):

        Server.__init__(self,*args,**kwargs)
        Log.Print("Starting server...")

        self.ip = kwargs["localaddr"][0]
        self.port = kwargs["localaddr"][1]
        self.svr_name = raw_input("Server name: ")
        while not MySQL.AddServer(self.svr_name,self.ip):
            Log.Print("Name allready exists")
            self.svr_name = raw_input("New name: ")
        MySQL.CheckDeadServers()
        ##### START UDP #####
        self.UDPconnector = ServerUDP(*args,**kwargs)
        self.UDPconnector.SetTarget(self)
        self.UDPconnector.SetPing(config.ping_server)

        self.id = 0
        self.mode = "Quickmatchs server"
        self.max_players = 10
        self.name = "Newtonis's server"
        self.clients = dict()
        self.players = dict()
        self.gameWorlds = dict()
        self.dictOrder = []

        self.play = True
        #self.commandsThread = threading.Thread(target=self.CommandThreadDef,name="Commands thread")
        #self.commandsThread.start()
        self.Add5Rooms()
        self.last_time_sql_updated = time.time()

    ##### UDP DEF #####
    def Network_UDP_data(self,data,addr):
        if not data.has_key("id"):
            Log.Print("Mysterious UDP data")
        if not self.clients.has_key(str(data["id"])):
            Log.Print("Mysterious UDP Data ID",data["id"])
        self.clients[data["id"]].udpAddr = addr
        if self.clients[data["id"]].addr[0] != addr[0]:
            Log.Print("Hacking from",addr,"trying to be player",data["id"])
        self.clients[data["id"]].collect_incoming_data(data["content"])
        self.clients[data["id"]].found_terminator()

    def Add5Rooms(self):
        #self.AddTestingGame("Testing area")
        for x in range(1):
            self.AddBasicGame("Friendly pitch "+str(x+1))
    def AddBasicGame(self,name):
        self.gameWorlds[name] = BasicGame(name)
        self.dictOrder.append(name)
    def AddTestingGame(self,name):
        self.gameWorlds[name] = TestingGame(name)
        self.dictOrder.append(name)
    def NextId(self):
        self.id += 1
        return self.id
        if len(self.clients) < self.max_players:
            allowed = True
            reason = ""
        else:
            allowed = False
            reason = "Server full"
        return allowed , reason
    def AllowEntrance(self):
        if len(self.clients) < self.max_players:
            allowed = True
            reason = ""
        else:
            allowed = False
            reason = "Server full"
        return allowed , reason
    def Connected(self , channel , addr):
        Log.Print("")
        Log.Print("Player connected (",addr,"), the id=",channel.id,"has just been assigned")
        Log.Print("Waiting to him to define if he'll play or only request information...")
        self.clients[channel.id] = channel
        channel.ip   = addr[0]
        channel.conn = addr[1]
    def LogicUpdate(self):
        self.Pump()
        for room in self.gameWorlds.keys():
            self.gameWorlds[room].LogicUpdate()
        if time.time() - self.last_time_sql_updated > 100:
            MySQL.UpdateServer(self.ip,self.svr_name)
            self.last_time_sql_updated = time.time()
    def CommandThreadDef(self):
        while self.play:
            command = raw_input("Command>")
            self.Command(command)
    def Command(self,com):
        if com == "exit":
            self.play = False
        elif com == "all-players":
            self.ShowAllPlayers()
        else:
            Log.Print("command",com," not found")
    def HandlePlayerLost(self,player):
        del self.clients[player.id]
    def ShowAllPlayers(self):
        pass
    def GetBasicInfo(self):
        allow , reason = self.AllowEntrance()
        return {"name":self.name,"mode":self.mode,"players":len(self.players.keys()),"max-players":self.max_players,"allow":allow,"reason":reason}
    def GetRoomsData(self):
        rooms = []
        for key in self.dictOrder:
            data = self.gameWorlds[key].GetBasicData()
            rooms.append(data)
        return rooms
    def JoinPlayer(self,player,room_name):
        self.gameWorlds[room_name].JoinPlayer(player)
    def GetPlayers(self):
        return Heads.heads
    def Close(self):
        Log.Print("Closing server ...")
        self.play = False
        self.UDPconnector.End()
