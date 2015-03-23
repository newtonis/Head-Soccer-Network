__author__ = 'newtonis'

import pygame
from source.data import fonts
from source.gui.window import Window
from source.gui.text import Text
from source.gui.input import Input
from source.gui.loading import LoadingAnimation
from source.gui.button import *
from source.gui.playerSelector import PlayerSelector

class ProfileSettings(Window):
    def __init__(self,parent):
        self.parent = parent
        Window.__init__(self,"Player select",(36, 107, 97),(43, 76, 111),0,0,500,250,(255,255,255))
        self.parent = parent
        self.parent.SetPlayersDef(self.DataPlayers)
        self.parent.SetProfileSettingsDef(self.NameConfirmation)
        self.Start()
    def Start(self,error=None):
        self.Send({"action":"req_av_players"})
        y_act = 40

        if error != None:
            error = Text(fonts.BebasNeue.c20,error,(255,0,0))
            error.x = self.width/2-error.surface.get_size()[0]/2
            error.y = y_act
            self.AddElement(error,"Error")
            y_act += error.surface.get_size()[1]+10

        textName = Text(fonts.BebasNeue.c30,"Player Name:",(255,255,255))
        textName.x = self.width/4-textName.surface.get_size()[0]/2
        textName.y = y_act
        self.AddElement(textName,"TextName")

        inputName = Input()
        inputName.x = self.width/4*3-inputName.size[0]/2
        inputName.y = y_act
        inputName.AllowAll()
        inputName.SetSize(200,30)
        self.AddElement(inputName,"inputName")
        y_act += 60

        loading = LoadingAnimation(0.4,5)

        loading.x = self.width/2-loading.width/2
        loading.y = y_act
        self.AddElement(loading,"LoadingA")
        y_act += 30

        loadingText = Text(fonts.BebasNeue.c20,"Loading players...",(255,255,255))
        loadingText.x = self.width/2-loadingText.surface.get_size()[0]/2
        loadingText.y = y_act
        self.AddElement(loadingText,"LoadingT")
        y_act += 70

        cancelButton = RejectButton("Cancel")
        cancelButton.x = self.width/2-cancelButton.imageA.get_size()[0]/2
        cancelButton.y = y_act
        self.AddElement(cancelButton,"CancelButton")
        y_act += cancelButton.size[1]

        self.SetHeight(y_act+10)
        self.originalPlayer = None

    def AddAcceptButton(self):
        self.references["CancelButton"].x = self.width/4 - self.references["CancelButton"].imageA.get_size()[0]/2
        acceptButton = AcceptButton("Accept")
        acceptButton.x = self.width/4*3-acceptButton.imageA.get_size()[0]/2
        acceptButton.y = self.references["CancelButton"].y
        self.AddElement(acceptButton,"AcceptButton")
    def DataPlayers(self,data):
        self.references["inputName"].text = data["player-name"]
        self.originalPlayer = data["player-name"]
        self.references["inputName"].letter_cursor = len(data["player-name"])
        self.references["inputName"].selected = True
        self.AddAcceptButton()
        self.DeleteElement("LoadingA")
        self.DeleteElement("LoadingT")
        selector = PlayerSelector(data["players"],self.width,100,self,(0,0))
        selector.x = self.width/2-selector.width/2
        selector.y = self.references["inputName"].y + self.references["inputName"].size[1] + 25
        selector.UpdateHead()
        if self.parent.serverDataCopy.has_key("headCode"):
            selector.SetCurrent(self.parent.serverDataCopy["headCode"])
        self.AddElement(selector,"Selector")
    def NameConfirmation(self,data):
        if data["error"] != "":
            self.DeleteElement("LoadingA")
            self.DeleteElement("LoadingT")
            self.Start(data["error"])
        else:
            self.parent.ReturnRoomListFP()
    def SetLoading(self):
        self.DeleteElement("TextName")
        self.DeleteElement("inputName")
        self.DeleteElement("CancelButton")
        self.DeleteElement("AcceptButton")
        self.DeleteElement("Selector")
        self.DeleteElement("Error")
        loading = LoadingAnimation(0.4,5)
        loading.x = self.width/2 - loading.width/2
        loading.y = self.height/2 - 10 - loading.height
        self.AddElement(loading,"LoadingA")
        loadingText = Text(fonts.BebasNeue.c20,"Checking name...",(255,255,255))
        loadingText.x = self.width/2 - loadingText.surface.get_size()[0]/2
        loadingText.y = self.height/2 + 10
        self.AddElement(loadingText,"LoadingT")

    def ExtraLogicUpdate(self):
        if self.ButtonCheck("CancelButton"):
            self.parent.ReturnRoomListFP()
        if self.ButtonCheck("AcceptButton"):
            name = self.references["inputName"].text
            if self.originalPlayer != None:
                if self.originalPlayer == name:
                    name = None
            self.Send({"action":"set_configuration","name":name,"headcode":self.references["Selector"].GetHeadCode()})
            self.parent.serverDataCopy["headCode"] = self.references["Selector"].GetHeadCode()
            self.SetLoading()

    def Send(self,data):
        self.parent.Send(data)