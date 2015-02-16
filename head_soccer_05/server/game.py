__author__ = 'newtonis'

from source.physics import game
import time
from source.physics import gameV2
from source.physics.gameV2 import *
import stadiums



class Game:
    def __init__(self,name,stadium,mode,players,type="testing"):
        self.name = name
        self.stadium = stadium
        self.mode = mode
        self.players = players
        self.playA = []
        self.playB = []
        self.playing = False
        self.spectators = dict()
        self.ref = time.time()*1000

        self.gameEngine = gameV2.PowerGameEngine("server")
        self.gameEngine.AddPitch()
        self.gameEngine.loopEnabled = True
        self.gameEngine.updateFrec = 40
        self.ratioCurrent = 10
        self.currentCount = 0


        #### THIS VARIABLES ARE TO SAVE THE HALF TIME DATA ###
        self.scoreFirstHalf = None
        self.scoreSecondHalf = None
        self.scoreFinal = None


        self.ballID = self.gameEngine.AddBall((10,10))

        self.gameEngine.SetMaxPlayers(self.players["sideA"],self.players["sideB"])
        self.gameEngine.SetTarget(self)

        self.clientsPlayers = dict()
        self.queueInput = dict()

        self.movePlayers = True
        self.status = "waiting"
        self.type = type
        if self.type == "testing":
            self.gameEngine.AddCentralText("This room is on 'Testing' Mode","Bebas20")
        else:
            self.gameEngine.AddCentralText("Waiting for players...","Bebas20")

        self.matchIsBeingPlayed = False

        self.data_to_update = dict()
        self.position_of_update = dict()
    def JoinPlayer(self,player):
        player.SetRoomDef(self.PlayerData)
        self.spectators[player.id] = player
        self.SendAllData(player)
        self.SendToAll({"action":"sa","type":"marker update A","new score":self.gameEngine.scoreA})
        self.SendToAll({"action":"sa","type":"marker update B","new score":self.gameEngine.scoreB})
    def GetBasicData(self):
        return {"name":self.name,"stadium":self.stadium["name"],"mode":self.mode,"playing":self.playing,"players":self.GetPlayersData()}
    def GetPlayersData(self):
        return {"play":self.players,"clients":len(self.playA)+len(self.playB),"max-clients":self.players["sideA"]+self.players["sideB"]}
    def SendAllData(self,player):
        player.Send({"action":"initial_join","data_join":self.GetJoinInfo(),"pitch_data":self.PitchData(),"id":player.id})
    def GetJoinInfo(self):
        sideA = self.players["sideA"]
        sideB = self.players["sideB"]
        return {"availableA":sideA - len(self.playA) , "availableB":sideB - len(self.playB),"max-A":self.players["sideA"],"max-B":self.players["sideB"]}
    def StoreHalf(self):
        if not self.scoreFirstHalf:
            self.scoreFirstHalf = {"A":self.gameEngine.scoreA,"B":self.gameEngine.scoreB}
        else:
            self.scoreFinal = {"A":self.gameEngine.scoreA,"B":self.gameEngine.scoreB}
            shA = self.scoreFinal["A"]-self.scoreFirstHalf["A"]
            shB = self.scoreFinal["B"]-self.scoreFirstHalf["B"]
            self.scoreSecondHalf = {"A":shA,"B":shB}
    def PlayerData(self,player,type,data=None):
        if type == "exit":
            self.PlayerExit(player)
        elif type == "joinA":
            self.JoinA(player)
        elif type == "joinB":
            self.JoinB(player)
        elif type == "spectate":
            self.Spectate(player)
        elif type == "lost":
            self.PlayerExit(player)
        elif type == "keys":
            self.KeysPlayer(player,data["keys"],data["id"],data)
        elif type == "bc":
            #ping = time.time()-data["at"]
            self.UpdateBP(data["pos"],data["vel"])
            #for x in range(8):
            #    self.gameEngine.world.Step(1.0/40.0,10,10)
            #print time.time(),rr05(self.gameEngine.elements[self.ballID].body.position),rr05(self.gameEngine.elements[self.ballID].body.linearVelocity)
            #self.gameEngine.worldVersion += 1
            self.HandleUpdateMovement()
        elif type == "update_pos":
            self.data_to_update[data["player id"]] = {"positions":data["positions array"],"linearVelocity":data["lv array"]}
            self.position_of_update[data["player id"]] = 0
    def UpdateBP(self,pos,vel):
        if self.gameEngine.elements.has_key(self.ballID):
            print "Ball UPDATE"
            self.gameEngine.elements[self.ballID].body.position = pos
            self.gameEngine.elements[self.ballID].body.linearVelocity = vel
    def PlayerExit(self,player):
        if not self.spectators.has_key(str(player.id)):
            return
        print "Player",player.GetID(),"decided to quit room"

        del self.spectators[player.id]
        for playX in range(len(self.playA)):
            if self.playA[playX].id == player.id:
                print "Player",player.GetID(),"has abandoned the 'A' side"
                del self.playA[playX]
                self.gameEngine.RemoveTeamAName()
                if self.status == "waiting":
                    self.gameEngine.UpdatePlaysA(len(self.playA))
                elif self.IsInMatch():
                    if len(self.playA) == 0:
                        self.Alose()
                break
        for playX in range(len(self.playB)):
            if self.playB[playX].id == player.id:
                del self.playB[playX]
                self.gameEngine.RemoveTeamBName()
                if self.status == "waiting":
                    self.gameEngine.UpdatePlaysB(len(self.playB))
                elif self.IsInMatch():
                    if len(self.playB) == 0:
                        self.Blose()

                break
        if self.clientsPlayers.has_key(player.id):
            self.gameEngine.DeleteElement(self.clientsPlayers[player.id])
            del self.clientsPlayers[player.id]
    def IsInMatch(self):
        return self.matchIsBeingPlayed
    def Alose(self):
        print "The 'A' side cannot play anymore"
        #self.gameEngine.RemoveTeamAName()
        self.status = "skipRematchEnd"
        self.gameEngine.AddWord("W.O. "+self.gameEngine.BteamName+" wins",(100,50,50),20,"Boombox20")
        self.gameEngine.StopClock(True)
        self.gameEngine.DeleteElement(self.ballID)
    def Blose(self):
        print "The 'B' side cannot play anymore"
        #self.gameEngine.RemoveTeamBName()
        self.status = "skipRematchEnd"
        self.gameEngine.AddWord("W.O. "+self.gameEngine.AteamName+" wins",(100,50,50),20,"Boombox20")
        self.gameEngine.StopClock(True)
        self.gameEngine.DeleteElement(self.ballID)
    def PlayerLost(self,player):
        self.PlayerExit(player)
    def JoinA(self,player):
        if len(self.playA) < self.players["sideA"]:
            print "Player",player.GetID(),"joined 'A' side"
            self.queueInput[player.id] = []
            id = self.gameEngine.AddPlayer(player.head,'A1')
            player.Send({"action":"sa","type":"confirm_join","element_id":id})
            self.playA.append(player)
            self.clientsPlayers[player.id] = id
            self.gameEngine.UpdatePlaysA(len(self.playA))
            self.gameEngine.SetATeamName(player.name)
            if self.type == "Real":
                self.CheckStart()
        else:
            print "'A' side is full so player",player.GetID(),"cannot join"
            self.SendFull(player)
    def JoinB(self,player):
        if len(self.playB) < self.players["sideB"]:
            print "Player",player.GetID(),"joined 'B' side"
            self.queueInput[player.id] = []
            id = self.gameEngine.AddPlayer(player.head,'A2')
            player.Send({"action":"sa","type":"confirm_join","element_id":id})
            self.playB.append(player)
            self.clientsPlayers[player.id] = id
            self.gameEngine.UpdatePlaysB(len(self.playB))
            self.gameEngine.SetBTeamName(player.name)

            if self.type == "Real":
                self.CheckStart()
        else:
            print "'B' side is full so player",player.GetID(),"cannot join"
            self.SendFull(player)
    def CheckStart(self):
        if len(self.playA) == self.players["sideA"] and len(self.playB) == self.players["sideB"]:
            self.matchIsBeingPlayed = True
            self.status = "WS"
    def Spectate(self,player):
        print "Player",player.GetID(),"joined as 'spectator'"
        player.Send({"action":"sa","type":"confirm_join"})
    def SendFull(self,player):
        player.Send({"action":"sa","type":"full_area"})
    def SendToAllUDP(self,data):
        #print data,"sent in UDP mode"
        for spectator in self.spectators.keys():
            self.spectators[spectator].SendUDP(data)
    def SendToAllUDPExcept(self,client_id,data):
        for spectator in self.spectators.keys():
            if spectator != client_id:
                self.spectators[spectator].SendUDP(data)
    def SendToAll(self,data):
        for spectator in self.spectators.keys():
            self.spectators[spectator].Send(data)
    def LogicUpdate(self):
        self.gameEngine.LogicUpdate()

        #### MANAGMENT OF THE GAME STATUS ####
        #print self.status
        if self.status == "WS":

            self.gameEngine.AddClock()
            self.gameEngine.AddScore()
            self.gameEngine.ResetPlayersPositions()

            self.gameEngine.DisableMaxPlayers()
            self.gameEngine.DeleteElement(self.ballID)
            self.gameEngine.StartGame()
            self.gameEngine.EnableMove()
            self.gameEngine.StartSequence()

            self.status = "countdown"
        elif self.status == "countdown":
            if self.gameEngine.numberSequence == 0:
                self.gameEngine.PlayClock()
                #self.gameEngine.StartGame()
                self.gameEngine.DeleteCentralText()
                self.playing = True
                self.ballID = self.gameEngine.AddBall()
                self.status = "playing"

        elif self.status == "playing":
            if self.gameEngine.clock.GetStatus() == "half":
                self.playing = False
                self.status = "WSH"
                self.gameEngine.DeleteElement(self.ballID)
                self.gameEngine.StopClock(True)
                self.gameEngine.AddWord("Halftime",(100,100,200),20)
                self.refWait = time.time() * 1000
                self.StoreHalf()
            elif self.gameEngine.clock.GetStatus() == "final":
                print "End of the match"
                self.playing = False
                self.status = "endRematch"
                self.gameEngine.StopClock(True)
                self.gameEngine.DeleteElement(self.ballID)
                self.gameEngine.AddWord(self.gameEngine.GetWinnerText(),(50,100,50),20,"Boombox20")
                self.StoreHalf()
        elif self.status == "WSH":
            if time.time() * 1000 - self.refWait > 3000:
                self.gameEngine.StartSequence()
                self.status = "countdown"
        elif self.status == "sequenceStart":
            if self.gameEngine.numberSequence == 0:
                self.gameEngine.PlayClock()
                self.gameEngine.AddBall()
                self.status = "playing"
        elif self.status == "Goal Scored":
            self.gameEngine.StopClock(True)
            self.status = "GSW"
        elif self.status == "GSW":
            if time.time()*1000 - self.refWait > 3000:
                self.gameEngine.StartSequence()
                self.gameEngine.DeleteElement(self.ballID)
                self.gameEngine.ResetPlayersPositions()
                self.status = "countdown"

        elif self.status == "endRematch": ### wait 3 seconds and go to rematch window
            self.HandleEndMatch(self.gameEngine.GetWinnerText())
            if time.time() * 1000 - self.refWait > 3000:
                self.status = "rematch"
                self.refWait = time.time() * 1000
        elif self.status == "rematch": ## wait 20 seconds and go to join window if no rematch is decided
            if time.time() * 1000 - self.refWait > 20000:
                self.status = "final_end"


        elif self.status == "skipRematchEnd":
            self.matchIsBeingPlayed = False
            self.refWait = time.time() * 1000
            self.status = "waitEnd" #wait 3 seconds to go to join Window
        elif self.status == "waitEnd":
            self.matchIsBeingPlayed = False
            if time.time() * 1000 - self.refWait > 3000:
                self.status = "final_end" #go to join window
        elif self.status == "final_end":
            self.EndMatch()
            self.SendJoinWindowToAll()
            self.status = "waiting"
            #self.gameEngine.AddWord(self.gameEngine.GetWinnerText(),(100,200,100),20,"Boombox40",-1)
    def SendJoinWindowToAll(self):
        self.SendToAll({"action":"sa","type":"joinWindow","data_join":self.GetJoinInfo()})
    def EndMatch(self):
        print "End match"
        self.playA = []
        self.playB = []
        for k in self.clientsPlayers.keys():
            self.gameEngine.DeleteElement(self.clientsPlayers[k])
            del self.clientsPlayers[k]

        self.gameEngine.RemoveBothNames()

        self.gameEngine.RemoveClock()
        self.gameEngine.DeleteScore()
        self.gameEngine.SetMaxPlayers(self.players["sideA"],self.players["sideB"])
        self.gameEngine.UpdatePlaysA(len(self.playA))
        self.gameEngine.UpdatePlaysB(len(self.playB))
        self.scoreFirstHalf = None
        self.scoreSecondHalf = None
        self.scoreFinal = None

    def HandleUpdateMovement(self):

        data_to_all = []
        for ball in self.gameEngine.balls:
            pos = rr05(self.gameEngine.elements[ball].body.position)
            lv = rr05(self.gameEngine.elements[ball].body.linearVelocity)
            data_to_all.append(self.GetElementMoveData(ball,pos,lv,True))

        for client_key in self.clientsPlayers.keys():
            element_id = self.clientsPlayers[client_key]
            if not self.gameEngine.elements.has_key(element_id):
                continue

            position = rr05(self.gameEngine.elements[element_id].body.position)
            velocity = rr05(self.gameEngine.elements[element_id].body.linearVelocity)

            data_to_all.append(self.GetElementMoveData(element_id,position,velocity))

        self.SendToAllUDPExcept(-1,{"action":"sa","type":"multiple-me","mes":data_to_all})
    ##### GAME TARGET DEF #####
    def HandleGoalScored(self,team):
        if self.playing:
            if team == "GoalA":
                self.gameEngine.GiveGoalB()
            elif team == "GoalB":
                self.gameEngine.GiveGoalA()
            self.status = "Goal Scored"
            self.refWait = time.time()*1000
    def HandleNewScore(self,side,score):
        if side == "A":
            self.SendToAll({"action":"sa","type":"marker update A","new score":self.gameEngine.scoreA})
        elif side == "B":
            self.SendToAll({"action":"sa","type":"marker update B","new score":self.gameEngine.scoreB})
    def TeamANameSet(self,name):
        self.SendToAll({"action":"sa","type":"nsA","name":name})
    def TeamBNameSet(self,name):
        self.SendToAll({"action":"sa","type":"nsB","name":name})
    def TeamANameOut(self):
        self.SendToAll({"action":"sa","type":"rmA"})
    def TeamBNameOut(self):
        self.SendToAll({"action":"sa","type":"rmB"})
    def NamesRemoved(self):
        self.SendToAll({"action":"sa","type":"rm"})
    def HandlerMaxPlayers(self,maxA,maxB):
        self.SendToAll({"action":"sa","type":"mp","maxA":maxA,"maxB":maxB})
    def DynamicElementAdded(self,element,id):
        element["id"] = id
        self.SendToAll({"action":"sa","type":"ae","cd":element})
    def DynamicElementDeleted(self,id):
        self.SendToAll({"action":"sa","type":"ed","id":id})
    def GetElementMoveData(self,id,position,lv,sendVersion=False,kid=-1):
        if sendVersion:
            data = {"action":"sa","type":"me","id":id,"p":position,"lv":lv,"ver":self.gameEngine.worldVersion}
        else:
            data = {"action":"sa","type":"me","id":id,"p":position,"lv":lv}
        return data
    def HandleElementMove(self,client_id,id,position,lv,sendVersion=False,kid=-1):
        if sendVersion:
            self.SendToAllUDPExcept(client_id,{"action":"sa","type":"me","id":id,"p":position,"lv":lv,"ver":self.gameEngine.worldVersion})
        else:
            self.SendToAllUDPExcept(client_id,{"action":"sa","type":"me","id":id,"p":position,"lv":lv})
    def HandleChangePlays(self,side,value):
        self.SendToAll({"action":"sa","type":"up","side":side,"value":value})
    def HandleScoreDeleted(self):
        self.SendToAll({"action":"sa","type":"removeScore"})
    def HandleScoreAdded(self):
        self.SendToAll({"action":"sa","type":"addScore"})
    def HandleDisableMax(self):
        self.SendToAll({"action" :"sa","type":"disableMax"})
    def HandleShowClock(self):
        self.SendToAll({"action":"sa","type":"enableClock"})
    def HandleRemoveClock(self):
        self.SendToAll({"action":"sa","type":"disableClock"})
    def HandlePlayClock(self):
        print "PlayClock"
        self.SendToAll({"action":"sa","type":"playClock"})
    def HandleStopClock(self,instant):
        self.SendToAll({"action":"sa","type":"stopClock","instant":instant})
    def HandleStartSequence(self):
        self.SendToAll({"action":"sa","type":"startSeq"})
    def SendPlayerHistory(self,id,history):
        self.SendToAll({"action":"sa","type":"history","id":id,"data":history})
    def HandleAddText(self,text,font,y):
        self.SendToAll({"action":"sa","type":"centralMSJ","text":text,"font":font,"y":y})
    def HandleRemoveText(self):
        self.SendToAll({"action":"sa","type":"removeTEXT"})
    def HandleStartGame(self):
        self.SendToAll({"action":"sa","type":"startGame"})
    def HandleCentralWord(self,word,color,time,font):
        self.SendToAll({"action":"sa","type":"BigWord","word":word,"color":color,"time":time,"font":font})
    def HandleRemoveCentralWord(self):
        self.SendToAll({"action":"sa","type":"removeWord"})
    def HandleEndMatch(self,textWin):
        print self.GetGoalsData()
        self.SendToAll({"action":"sa","type":"final","wData":{"goalsData":self.GetGoalsData(),"textWin":textWin}})
    ##### END GAME TARGET DEF #####
    def KeysPlayer(self,player,keys,kid,data):
        if not self.movePlayers:
            return

        if self.clientsPlayers.has_key(player.id):
            id = self.clientsPlayers[player.id]
            self.gameEngine.elements[id].UpdateActions(keys)


 #### UDP CAN FAIL OFTEN ####
    def PitchData(self):
        return self.gameEngine.GetData()
    def GetGoalsData(self):
        return {"FH":self.scoreFirstHalf,"SH":self.scoreSecondHalf,"FN":self.scoreFinal}

class BasicGame(Game):
    def __init__(self,name):
        Game.__init__(self,name,stadiums.ORTSoccer,"1vs1 friendly",{"sideA":1,"sideB":1},"Real")

class TestingGame(Game):
    def __init__(self,name):
        Game.__init__(self,name,stadiums.ORTSoccer,"1vs1 testing",{"sideA":1,"sideB":1},"testing")