__author__ = 'newtonis'

from PodSixNet.Connection import connection, ConnectionListener
from PodSixNet.ClientUDP import ClientUDP
import pygame
import time
from pygame.color import THECOLORS
from game import *

pygame.font.init()
font = pygame.font.Font("fonts/VCR_OSD_MONO.ttf" , 50)

class Game(ConnectionListener):
    def __init__(self,host,port):
        self.Connect((host,port))
        self.UDPconnection = ClientUDP(host,port)
        self.UDPconnection.SetTarget(self)
        print "Connecting to ",host,":",port
        self.host = host
        self.port = port

        self.clock = pygame.time.Clock()
        self.fps   = 40
        self.time  = 0
        self.players = dict()

        self.play = True
        self.retry= False
        self.playing = False
        self.game  = Game_handler((900,600),"Head soccer client 0.1")
        self.game.add_pitch("l0","l1","l2")
        ##self.game.SetFps(40)

        self.screen = self.game.screen
        self.my_id = -1
        self.object_id = -1
        self.goalsA = 0
        self.goalsB = 0
        self.surfaceGoalsA = self.CreateGoalsSurface(self.goalsA)
        self.surfaceGoalsB = self.CreateGoalsSurface(self.goalsB)
        self.loops = 0
        self.update_rate = 1
        self.CentralMessage = "Connecting ..."
        self.SizeCentral    = 30
        self.centralFont    = font
        self.UpdateCentralMessage(self.CentralMessage,self.SizeCentral)
    def CreateGoalsSurface(self,goals):
        return font.render(str(goals),0,(255,255,255))
    def AddToPitch(self,data):
        for object in data:
            self.Add(object)
    def Add(self,object):
        if object["type"] == "head":
            self.AddPlayer(object)
        elif object["type"] == "ball":
            self.AddBall(object)
    def AddPlayer(self,object):
        print object["position"]
        head = Head(object["position"],object["head"],self.game)
        head.SetLinearVelocity(object["linearVelocity"])
        self.game.add_element(head ,object["id"])
    def AddBall(self,cont):
        e = self.game.add_element(Element("ball",self.game.world.CreateDynamicBody(position=cont["position"] , linearVelocity=cont["linearVelocity"] , bullet=True ), self.game  , ball),cont["id"])
        circle = e.body.CreateCircleFixture(radius=0.475, density=200, friction=0.1 ,restitution=0.95)
        self.game.ball = circle
    def Launch(self):
        while self.play:
            dt_s = float(self.clock.tick(self.fps)*1e-3)
            if dt_s >= 0.10:
                continue
            self.Pump()
            connection.Pump()
            self.Events()
            self.game.update()
            self.game.update_goals()
            self.Draw()

            self.time += dt_s
            self.loops += 1
        if self.retry:
            self.retry = False
            time.sleep(10)
            print "Retry ..."
            self.__init__(self.host,self.port)
            self.Launch()
        self.UDPconnection.End()
    def Draw(self):
        self.game.clear()
        self.game.draw()
        self.DrawScore()
        self.DrawCentral()
        self.game.refresh()
    def DrawScore(self):
        self.screen.blit(self.surfaceGoalsB,(100-self.surfaceGoalsA.get_size()[0]/2,40))
        self.screen.blit(self.surfaceGoalsA,(800-self.surfaceGoalsB.get_size()[0]/2,40))
    def DrawCentral(self):
        self.screen.blit(self.CentralSurface,(self.screen.get_size()[0]/2-self.CentralSurface.get_size()[0]/2 , 280))
    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.play = False
        keys = pygame.key.get_pressed()

        if self.playing:
            self.UpdateEvents(keys[pygame.K_UP],keys[pygame.K_LEFT],keys[pygame.K_RIGHT],keys[pygame.K_SPACE])
    def ScoreA(self):
        self.goalsA += 1
        self.surfaceGoalsA = self.CreateGoalsSurface(self.goalsA)
    def ScoreB(self):
        self.goalsB += 1
        self.surfaceGoalsB = self.CreateGoalsSurface(self.goalsB)
    def UpdateEvents(self , up , left , right , kick):
        actions = {"jump":up,"left":left,"right":right,"kick":kick}
        self.game.elements[self.object_id].move_manual(actions)
        self.SendUDP({"action":"update_events","events":actions})
        #self.Send({"action":"update_events","events":{"jump":up,"left":left,"right":right,"kick":kick}})
    def SendUDP(self,data):
        if self.my_id == -1:
            print "Can't send UDP data because id=-1"
        self.UDPconnection.Send(data,self.my_id)
    def Network_UDP_data(self,data):
        connection.Network(data)
    def Newtork_socketConnect(self):
        print "connected!"
    def Network_initial(self,data):
        print "Network pitch data received"
        self.my_id = data["id"]
        self.AddToPitch(data["content"])
        self.goalsA = data["score"]["A"]
        self.goalsB = data["score"]["B"]
        self.Send({"action":"request_play","side":1})
        self.UpdateCentralMessage(data["message"],data["size"])
    def UpdateCentralMessage(self,message,size):
        self.CentralMessage = message
        if size != self.SizeCentral:
            self.centralFont = pygame.font.Font("fonts/VCR_OSD_MONO.ttf",size/2)
        self.SizeCentral = size
        self.CentralSurface = self.centralFont.render(message,0,(255,255,255))
    def Network_score(self,data):
        if data["side"] == 1:
            self.ScoreA()
        elif data["side"] == 2:
            self.ScoreB()
    def Network_new_element(self,data):
        self.Add(data["element"])
    def Network_delete_element(self,data):
        self.game.delete_element(data["id"])
    def Network_cp(self,data):
        try:
            if data["id"] == self.object_id or self.game.elements[data["id"]].way == "ball":
                if self.loops % self.update_rate != 0:
                    return
            self.game.elements[data["id"]].body.position = data["p"]
            if data.has_key("lv"):
                self.game.elements[data["id"]].body.linearVelocity = data["lv"]
        except:
            print "bad pack"
    def Network_result_join(self,data):
        if data["result"] != "nojoin":
            self.playing = True
            self.object_id = data["playerID"]
            print "Playing"
    def Network_disconnected(self,data):
        print "Server connection lost ..."
        print "Ending"
        #self.UpdateCentralMessage("**Network trouble**",30)

        self.play = False
        self.retry= False
    def Network_update_message(self,data):
        self.UpdateCentralMessage(data["message"],data["size"])
    def Network_error(self,data):
        print data
        self.UpdateCentralMessage(data["error"][1],30)
        self.play = False
        self.retry= True
        print "Retry in 10 seconds ..."
    def Network(self,data):
        if data["action"] != "cp":
            print data

def main():
    host = raw_input("host:")
    port = 9999
    game = Game(host,port)
    game.Launch()

if __name__ == "__main__":
    main()
