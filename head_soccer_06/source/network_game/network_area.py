__author__ = 'newtonis'

import pygame
from source.data import fonts
from source.gui.container import Container
from source.gui.button import NeutralButton
from source.gui.text import Text
from source.physics.gameV2 import *
from source.network_game.join_window import JoinWindow
from source.network_game.match_final_window import MatchFinalWindow
from source.network_game.ping.utils import *
from source.network_game.ping.ping_window import *
import time


class NetworkArea(Container):
    def __init__(self,initial_data,parent):
        Container.__init__(self)
        self.parent = parent

        print "The pitch type is '"+str(initial_data["pitch_data"]["pitch_name"])+"'"
        print "Pitch dynamic content:",initial_data["pitch_data"]["pitch_content"]
        parent.AddWindowCenteredOnFront(JoinWindow(initial_data["data_join"]),None,"joinWindow")

        self.parent.SetStageActionDef(self.NetworkAction)

        self.game = PowerGameEngine("client")
        self.game.SetClientTarget(self)
        self.game.SetData(initial_data["pitch_data"])

        self.game.loopEnabled = False
        self.parent.SendUDP({"action":"none"})
        self.SendEvents = False
        self.timeEvt = 0
        self.waitingVersion = False

        self.playerData = dict()
        self.playerMovement = dict()
        self.refUpdate = time.time()*1000
        self.playerID = -1
        self.positions_to_send = []
        self.lv_to_send = []

        self.currentPing = 0
        self.needTake = True
        self.takeSent = 0
        self.lastPingShown = None

        self.waiting_for_colition = {"waiting":False,"time":time.time()}

        self.NeedConfirm = dict()
        self.AddExitButton()
        self.AddPingNumber()

        self.pingStatus = "normal"
        self.maxSupportedPing = 500
        self.fixedPing = 500
    def AddPingNumber(self):
        pingText = Text(fonts.Absender.c20,"       ",(0,0,0))
        pingText.x = self.game.pixelWidth - 20 - pingText.surface.get_size()[0]
        pingText.y = 10
        self.Add(pingText,"PingText")
    def AddExitButton(self):
        button = NeutralButton("Exit",width=100,font=fonts.BebasNeue.c20)
        button.x = 20
        button.y = 10
        self.Add(button,"ExitButton")
    def LogicUpdate(self):

        Container.LogicUpdate(self)
        if self.ButtonCheck("ExitButton") and not self.parent.noCheckExit:
            self.parent.OpenCheckExit()

        if self.waiting_for_colition["waiting"]:
            print "WAITING"
            if time.time() - self.waiting_for_colition["time"] > .3:
                self.waiting_for_colition["waiting"] = False

        self.game.LogicUpdate()

        if self.SendEvents:
            keys = pygame.key.get_pressed()

            if self.playerID != -1 and self.game.elements.has_key(self.playerID):

                data = dict()
                if keys[pygame.K_UP]:
                    data["up"] = True
                if keys[pygame.K_LEFT]:
                    data["left"] = True
                if keys[pygame.K_RIGHT]:
                    data["right"] = True

                self.SendKeys(data , self.game.elements[self.playerID].body.position , self.game.elements[self.playerID].body.linearVelocity)
        self.UpdatePingValue()
    def UpdatePingValue(self):
        pingValue = self.GetPing()
        if not self.lastPingShown or self.lastPingShown != pingValue:
            self.Ereferences["PingText"].text = gPingText(pingValue)
            self.Ereferences["PingText"].color = gPingColor(pingValue)
            self.Ereferences["PingText"].Render()
        if self.SendEvents:
            if self.pingStatus == "highPing":
                self.parent.references["pingWindow"].SetPing(pingValue)
                if pingValue <= self.maxSupportedPing:
                    self.pingStatus = "normal"
                    self.parent.Kill(self.parent.references["pingWindow"])
            elif self.pingStatus == "normal":
                if pingValue > self.maxSupportedPing:
                    self.pingStatus = "highPing"
                    self.parent.AddWindowCenteredOnFront(PingWindow(),None,"pingWindow")

    def SendKeys(self,keys,pos,vel):
        self.timeEvt += 1
        self.NeedConfirm[str(self.timeEvt)] = keys
        cc = self.RegisterSent()
        self.SendUDP({"action":"keys","keys":keys,"id":self.timeEvt,"pos":rr05(pos),"vel":rr05(vel),"cc":cc})
    def RegisterSent(self):
        if self.needTake:
            self.needTake = False
            self.takeSent = time.time()*1000
            return 1
        return 0
    def RegisterRecv(self):
        self.needTake = True
        self.currentPing = time.time()*1000 - self.takeSent
    def GraphicUpdate(self,screen):
        self.game.GraphicUpdate(screen)

        Container.GraphicUpdate(self,screen)
    def PlayerCollision(self,player_position,player_lv,ball_position,ball_lv):
        pass
    def NetworkAction(self,data):
        if data["type"] == "ae": #### ADD ELEMENT ####
            self.game.CreateElement(data["cd"])
        elif data["type"] == "multiple-me":
            if data["cc"]:
                self.RegisterRecv()
            for x in data["mes"]:
                self.NetworkAction(x)
        elif data["type"] == "me": ### UPDATE ELEMENT POSITION ###
            self.game.UpdateElementPosition(data["id"],data["p"],data["lv"])
        elif data["type"] == "ed": ### ELEMENT DELETED ###
            self.game.DeleteElement(data["id"])
        elif data["type"] == "mp": ### UPDATE MAX PLAYERS ###
            self.game.SetMaxPlayers(data["maxA"],data["maxB"])
        elif data["type"] == "up": ### UPDATE PLAYER AMOUNT
            if data["side"] == 'A':
                self.game.UpdatePlaysA(data["value"])
            elif data["side"] == 'B':
                self.game.UpdatePlaysB(data["value"])
        elif data["type"] == "nsA": ### NAME A ###
            self.game.SetATeamName(data["name"])
        elif data["type"] == "nsB": ### NAME B ###
            self.game.SetBTeamName(data["name"])
        elif data["type"] == "rmA": ### REMOVE NAME A ###
            self.game.RemoveTeamAName()
        elif data["type"] == "rmB": ### REMOVE NAME B ###
            self.game.RemoveTeamBName()
        elif data["type"] == "rm": ### REMOVE BOTH NAMES ###
            self.game.RemoveBothNames()
        elif data["type"] == "confirm_join":
            if data.has_key("element_id"):
                self.SendEvents = True
                self.playerID = data["element_id"]
                self.game.elements[self.playerID].UnFreeze()
                self.game.SetPlayer(self.playerID)
            self.parent.DeleteAllWindows()
        elif data["type"] == "full_area":
            self.parent.references["joinWindow"].RejectJoin()
        elif data["type"] == "marker update A":
            print "score A",data
            self.game.SetScoreA(data["new score"])
        elif data["type"] == "marker update B":
            print "score B",data
            self.game.SetScoreB(data["new score"])
        elif data["type"] == "removeScore":
            self.game.DeleteScore()
        elif data["type"] == "addScore":
            self.game.AddScore()
        elif data["type"] == "disableMax":
            self.game.DisableMaxPlayers()
        elif data["type"] == "enableClock":
            self.game.AddClock()
        elif data["type"] == "disableClock":
            self.game.RemoveClock()
        elif data["type"] == "playClock":
            print "Play Clock"
            self.game.PlayClock()
        elif data["type"] == "stopClock":
            self.game.StopClock(ins=data["instant"])
        elif data["type"] == "startSeq":
            self.game.StartSequence()
        elif data["type"] == "history":
            self.ElementHistory(data["id"],data["data"])
        elif data["type"] == "centralMSJ":
            print "Add text",data["text"]
            self.game.AddCentralText(data["text"],data["font"],data["y"])
        elif data["type"] == "removeTEXT":
            self.game.DeleteCentralText()
        elif data["type"] == "startGame":
            self.game.StartGame()
        elif data["type"] == "confirmKeys":
            self.game.ConfirmKeys(data["id"])
        elif data["type"] == "BigWord":
            print "Add word"
            self.game.AddWord(data["word"],data["color"],data["time"],data["font"])
        elif data["type"] == "removeWord":
            print "Remove Word"
            self.game.RemoveWord()
        elif data["type"] == "final":
            print "Final Window"
            self.parent.AddWindowCenteredOnFront(MatchFinalWindow(data["wData"]),None,"finalWindow")
        elif data["type"] == "joinWindow":
            self.SendEvents = False
            self.parent.DeleteAllWindows()
            self.parent.AddWindowCenteredOnFront(JoinWindow(data["data_join"]),None,"joinWindow")
    def NetworkAddElement(self,data):
        element = data["element"]
        self.AddPitchElement(element)
    def NetworkDeleteElement(self,data):
        pass
        #self.RemoveElement(data["id"])
    def NetworkUpdateElementStatus(self,data):
        pass
    def SendUDP(self,data):
        self.parent.SendUDP(data)
    def ElementHistory(self,id,data):
        if len(data) == 0:
            return
        return
        if id == self.playerID:
            last_data = data[-1]
            moment = str(last_data["id"])

            pos_moment_self = self.playerData[moment]["pos"]
            vel_moment_self = self.playerData[moment]["vel"]

            for key in self.playerMovement.keys():
                if int(key) < int(moment):
                    del self.playerMovement[key]
                    del self.playerData[key]

            pos_moment_server = last_data["pos"]
            vel_moment_server = last_data["vel"]

            if pos_moment_server != pos_moment_self or vel_moment_server != vel_moment_self: ### DESINCRONIZACION ###
                print "resynchronizing..."
                self.game.elements[self.playerID].body.position = pos_moment_server
                self.game.elements[self.playerID].body.velocity = pos_moment_self

                for x in range(int(moment),self.timeEvt+1):
                    self.game.world.Step(self.game.TIME_STEP,10,10)
    def GetPing(self):

        if time.time()*1000-self.takeSent > 3000:
            self.RegisterRecv()
        last_ping = self.currentPing
        return last_ping

