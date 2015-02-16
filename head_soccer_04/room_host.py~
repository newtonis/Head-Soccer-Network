__author__ = 'ariel'

import sys
import pygame
import socket
import time

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.ServerUDP import ServerUDP

import images
from game import *
import random

class ServerChannel(Channel):
    def __init__(self , *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())
        intid = int(self.id)
        self.name = "Player " + str(self.id)

        self.events = {"jump":False,"left":False,"right":False,"kick":False}
        self.type     = "spectator"
        self.position = [0,0]
        self.my_player= None
        self.udpAddr = -1
        self.updateT = 40
        self.loops   = 0
    def Close(self):
        self._server.handle_player_lost(self)
    def Network_update_events(self , data):
        self.events = data["events"]
    def Network_set_name(self,data):
        self.name = data["name"]
    def Network_request_play(self,data):
        side = data["side"]
        self._server.handle_request_play( side , self)
    def Event(self ,key):
        return self.events[key]
    def GetInfo(self):
        if self.my_player == None:
            return {"id":self.id,"name":self.name,"playing":False}
        else:
            return {"id":self.id,"name":self.name,"playing":True,"head": self.my_player.head,"po":self._server.RoundSend(self.my_player.body.position)}
    def Loop(self):

        if self.my_player != None:
            self.my_player.move_manual( self.events )
            #if self.loops % self.updateT == 0:
            self._server.SendToAllUDP({"action":"cp","id":self.my_player.id,"p":self._server.RoundSend(self.my_player.body.position),"lv":self._server.RoundSend(self.my_player.body.linearVelocity)})
            #self.loops += 1
    def SendUDP(self,data):
        if self.udpAddr != -1:
            self._server.UDPconnector.Send(data,self.udpAddr)

class WhiteboardServer(Server):
    channelClass = ServerChannel
    def __init__(self,*args,**kwargs):
        print "Starting server ..."
        self.id = 0
        self.objects_id = 0
        Server.__init__(self,*args,**kwargs)
        self.UDPconnector = ServerUDP(*args,**kwargs)
        self.UDPconnector.SetTarget(self)


        self.clock = pygame.time.Clock()
        self.players = dict()

        self.spectators = []
        self.playingA   = []
        self.playingB   = []
        self.max_side   =  1

        self.game = Game_handler((900,600),"Head soccer server 0.1")
        self.game.add_pitch(self.NextObjectsId(),self.NextObjectsId(),self.NextObjectsId())
        self.game.SetTarget(self)
        self.play    = True
        self.start   = False
        self.scoreA  = 0
        self.scoreB  = 0
        self.time    = 0
        self.ball    = None
        self.timeREF = 0
        self.status  = "playing"
        self.lastGoal = 0
        self.CentralMessage = "Waiting for players ..."
        self.SizeCentral    = 30
    def Network_UDP_data(self,data,addr):
        if not self.players.has_key(data["id"]):
            return
        self.players[data["id"]].udpAddr = addr
        if self.players[data["id"]].addr[0] != addr[0]:
            print "Hacking !!!! from ",addr," trying to be player",data["id"]
            return
        self.players[data["id"]].collect_incoming_data(data["content"])
        self.players[data["id"]].found_terminator()
    def UpdateMessage(self,message,size):
        self.CentralMessage = message
        self.SizeCentral    = size
        self.SendToAll({"action":"update_message","message":message,"size":size})
    def NextId(self):
        self.id += 1
        return self.id
    def NextObjectsId(self):
        self.objects_id += 1
        return self.objects_id
    def Connected(self , channel , addr):
        print "Player connected (",addr,")"
        channel.Send({"action":"initial" , "content":self.GetPlayingInfo(),"id":channel.id,"score":self.GetScores(),"message":self.CentralMessage,"size":self.SizeCentral})
        self.players[channel.id] = channel
    def GetPlayingInfo(self):
        info = []
        for pk in self.game.elements.keys():
            element = self.game.elements[pk]
            info.append( element.GetCode() )
        return  info
    def SendToAllUDP(self,data):
        for pk in self.players.keys():
            player = self.players[pk]
            player.SendUDP(data)
    def SendToAll(self,data):
        for pk in self.players.keys():
            player = self.players[pk]
            player.Send(data)
    def Loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.play = False

        self.game.update()
        self.LoopPlayers(self.playingA)
        self.LoopPlayers(self.playingB)
        if self.start:
            self.SendUpdateBallPosition()
            if self.status == "scored":
                if time.time() - self.timeREF > 3.0:
                    self.UpdateMessage("",20)
                    self.status = "playing"
                    self.game.delete_element(self.ball.id)
                    self.players[ self.playingA[0] ].my_player.body.position = (3,1)
                    self.players[ self.playingB[0] ].my_player.body.position = (30,1)

                    self.SendToAll({"action":"delete_element","id":self.ball.id})
                    self.ball = self.game.add_ball(self.NextObjectsId() , self.GetBallSide())
                    self.SendToAll({"action":"new_element","element":self.ball.GetCode()})

    def RoundSend(self,value):
        return value[0],value[1]
        #return float(int(value[0]*10))/10.0 , float(int(value[1]*10))/10.0
    def SendUpdateBallPosition(self):

        self.SendToAllUDP({"action":"cp","id":self.ball.id,"p":self.RoundSend(self.ball.body.position),"lv":self.RoundSend(self.ball.body.linearVelocity)})
    def LoopPlayers(self,players):
        for pk in players:
            player = self.players[pk]
            player.Loop()
    def Draw(self):
        self.game.clear()
        self.game.draw()
        self.game.refresh()
    def Launch(self):
        while self.play:
            self.Pump()
            self.Loop()
            self.Draw()
        self.UDPconnector.close()
    def handle_player_lost(self,player):
        if player.type == "playerA":
            pass
        elif player.type == "playerB":
            pass
        elif player.type == "spectator":
            pass
    def handle_request_play(self,side,player):
        #if self.start:
         #    player.Send({"action":"result_join" , "result":"nojoin"})
        if side == 1:
            if len(self.playingA) < self.max_side: #if there is space
                self.JoinA(player)
            elif len(self.playingB) < self.max_side:
                self.JoinB(player)

        elif side == 2:
            if len(self.playingB) < self.max_side:
                self.JoinA(player)
            elif len(self.playingA) < self.max_side:
                self.JoinB(player)
        self.CheckStart()

    def JoinA(self,player):
        self.playingA.append(player.id)
        player.type      = "player A"
        player.my_player = self.game.add_player_A(self.NextObjectsId())
        player.head      = "head B"
        player.Send({"action":"result_join" , "result":"join A","playerID":player.my_player.id})
        self.SendToAll({"action":"new_element","element":player.my_player.GetCode()})

    def JoinB(self,player):
        self.playingB.append(player.id)
        player.type      = "player B"
        player.my_player = self.game.add_player_B(self.NextObjectsId())
        player.head      = "head A"
        player.Send({"action":"result_join" , "result":"join B","playerID":player.my_player.id})
        self.SendToAll({"action":"new_element","element":player.my_player.GetCode()})

    def AddBall(self):
        self.ball = self.game.add_ball(self.NextObjectsId() , self.GetBallSide())
        self.SendToAll({"action":"new_element","element":self.ball.GetCode()})
    def StartMatch(self):
        print "starting match"
        self.AddBall()
    def CheckStart(self):
        if self.start == False:
            if len(self.playingA) == self.max_side and len(self.playingB) == self.max_side:
                self.UpdateMessage("",20)
                self.StartMatch()
                self.start = True
            else:
                self.UpdateMessage("Waiting for "+str(self.max_side-len(self.playingA)+self.max_side-len(self.playingB))+" more players" ,20)
    def GetBallSide(self):
        if self.lastGoal == 0:
            return random.randrange(1,3)
        else:
            return self.lastGoal
    def ScoreA(self):
        if self.status != "playing":
            return
        self.UpdateMessage("GOAL!",80)
        self.status = "scored"
        self.scoreA += 1
        self.SendToAll({"action":"score","side":1})
        self.timeREF = time.time()
        self.lastGoal = 1
    def ScoreB(self):
        if self.status != "playing":
            return
        self.UpdateMessage("GOAL!",80)
        self.status = "scored"
        self.scoreB += 1
        self.SendToAll({"action":"score","side":2})
        self.timeREF = time.time()
        self.lastGoal = 2
    def GetScores(self):
        return {"A":self.scoreA,"B":self.scoreB}
    #def EnableGraphics(self):
    #    pass
def main():
    host = "localhost"
    port = 9999
    server = WhiteboardServer(localaddr=(host,port))
    server.Launch()

if __name__ == "__main__":
    main()
