__author__ = 'newtonis'

import time

from source.data import fonts
from source.gui.window import Window
from source.gui.text import Text
from source.gui.button import *
from source.gui.loading import LoadingAnimation

def Available(data):
    amount = data["availableA"] + data["availableB"]
    return amount > 0

def GetTextData(amount):
    if amount > 0:
        return "There are currently "+str(amount)+" places available" , (255,255,255)
    else:
        return "The pitch is currently Full" ,(255,0,0)

class JoinWindow(Window):
    def __init__(self,dataJoin):
        self.fullA = False
        self.fullB = False
        Window.__init__(self,"Join to game",(36, 107, 97),(36, 107, 97),0,0,500,140,(255,255,255),200)
        self.maxA = dataJoin["max-A"]
        self.maxB = dataJoin["max-B"]
        self.availableA = dataJoin["availableA"]
        self.availableB = dataJoin["availableB"]
        self.playsA = self.maxA - self.availableA
        self.playsB = self.maxB - self.availableB
        self.UpdatePlayersA(dataJoin["availableA"])
        self.UpdatePlayersB(dataJoin["availableB"])

        self.SS = "A"
        self.ref = time.time()*1000
    def CheckFull(self):
        self.available = self.availableA + self.availableB > 0

        self.statusA = "UNK"
        self.statusB = "UNK"

        self.SetTextInitial(GetTextData(self.availableA+self.availableB))

        if self.available:
            self.SetUpTextA(self.maxA-self.availableA)
            self.SetUpTextB(self.maxB-self.availableB)
            self.AddSpectate()
            self.UpdateButtons()
        else:
            self.fullA = False
            self.fullB = False
            self.DeleteElement("TextA")
            self.DeleteElement("TextB")
            self.AddSpectateB()
            self.AddQuitButton()

    def SetTextInitial(self,text):
        self.DeleteElement("textInitial")
        textInitial = Text(fonts.BebasNeue.c20,text[0],text[1])
        textInitial.x = self.width/2-textInitial.surface.get_size()[0]/2
        textInitial.y = 30
        self.AddElement(textInitial,"textInitial")
    def SetUpTextA(self,text):
        self.DeleteElement("TextA")
        text = Text(fonts.BebasNeue.c20,str(text)+"/"+str(self.maxA),(255,255,255))
        text.x = self.width/6 - text.surface.get_size()[0]/2
        text.y = 60
        self.AddElement(text,"TextA")
    def SetUpTextB(self,text):
        self.DeleteElement("TextB")
        text = Text(fonts.BebasNeue.c20,str(text)+"/"+str(self.maxB),(255,255,255))
        text.x = self.width/6*5 - text.surface.get_size()[0]/2
        text.y = 60
        self.AddElement(text,"TextB")
    def AddButtonA(self):
        self.fullA = False
        self.DeleteElement("ButtonA")
        button = AcceptButton("Join",width=100)
        button.x = self.width/6-button.imageA.get_size()[0]/2
        button.y = 90
        self.AddElement(button,"ButtonA")
    def AddFullA(self):
        self.fullA = True
        self.DeleteElement("ButtonA")
        signal = Text(fonts.BebasNeue.c30,"FULL",(255,0,0))
        signal.x = self.width/6-signal.surface.get_size()[0]/2
        signal.y = 90
        self.AddElement(signal,"ButtonA")
    def AddButtonB(self):
        self.fullB = False
        self.DeleteElement("ButtonB")
        button = AcceptButton("Join",width=100)
        button.x = self.width/6*5-button.imageB.get_size()[0]/2
        button.y = 90
        self.AddElement(button,"ButtonB")
    def AddFullB(self):
        self.fullB = True
        self.DeleteElement("ButtonB")
        signal = Text(fonts.BebasNeue.c30,"FULL",(255,0,0))
        signal.x = self.width/6*5-signal.surface.get_size()[0]/2
        signal.y = 90
        self.AddElement(signal,"ButtonB")
    def AddSpectate(self):
        self.DeleteElement("SpectateButton")
        button = NeutralButton("Spectate",width=150)
        button.x = self.width/2-button.imageA.get_size()[0]/2
        button.y = 90
        self.AddElement(button,"SpectateButton")
    def AddSpectateB(self):
        self.DeleteElement("SpectateButton")
        button = AcceptButton("Spectate")
        button.x = self.width/4-button.imageA.get_size()[0]/2
        button.y = 90
        self.AddElement(button,"SpectateButton")
    def AddQuitButton(self):
        self.DeleteElement("QuitButton")
        button = RejectButton("Exit")
        button.x = self.width/4*3-button.imageA.get_size()[0]/2
        button.y = 90
        self.AddElement(button,"Exit")
    def UpdateButtons(self):
        if self.playsA >= self.maxA and self.statusA != "FULL":
            self.statusA = "FULL"
            self.AddFullA()
        elif self.playsA < self.maxA and self.statusA != "AV":
            self.statusA = "AV"
            self.AddButtonA()

        if self.playsB >= self.maxB and self.statusB != "FULL":
            self.statusB = "FULL"
            self.AddFullB()
        elif self.playsB < self.maxB and self.statusB != "AV":
            self.statusB = "AV"
            self.AddButtonB()
    def SetTextLoading(self,text):
        loading_text = Text(fonts.BebasNeue.c40,text,(255,255,255))
        loading_text.x = self.width/2-loading_text.surface.get_size()[0]/2
        loading_text.y = 100
        self.AddElement(loading_text,"LoadingText")
    def UpdatePlayersA(self,available):
        self.availableA = available
        self.playsA = self.maxA - self.availableA
        self.CheckFull()
    def UpdatePlayersB(self,available):
        self.availableB = available
        self.playsB = self.maxB - self.availableB
        self.CheckFull()
    def ExtraLogicUpdate(self):
        #print time.time()*1000 - self.ref
        #if self.SS == "A":
        #    if time.time()*1000 - self.ref > 5000:
        #        self.UpdatePlayersA(0)
        #        self.SS = "B"
        #elif self.SS == "B":
        #    if time.time()*1000 - self.ref > 10000:
        #        self.UpdatePlayersB(0)
        #        self.SS = "C"

        if self.ButtonCheck("Exit"):
            self.parent.OpenCheckExit()
        if not self.fullA:
            if self.ButtonCheck("ButtonA"):
                self.SetLoading("Joining game")
                self.parent.JoinA()
        if not self.fullB:
            if self.ButtonCheck("ButtonB"):
                self.SetLoading("Joining game")
                self.parent.JoinB()
        if self.ButtonCheck("SpectateButton"):
            self.SetLoading("Joining as spectator")
            self.parent.Spectate()
        self.parent.AddUpdateRect(self.x,self.y,self.width,self.height+30)
    def SetLoading(self,text):
        self.DeleteElement("ButtonA")
        self.DeleteElement("ButtonB")
        self.DeleteElement("SpectateButton")
        self.DeleteElement("TextA")
        self.DeleteElement("TextB")
        la = LoadingAnimation(0.6,5)
        la.x = self.width/2-la.width/2
        la.y = 60
        self.AddElement(la,"LoadingAnimation")
        self.SetTextLoading(text)
    def RejectJoin(self):
        self.DeleteElement("LoadingAnimation")
        self.DeleteElement("LoadingText")
        self.CheckFull()