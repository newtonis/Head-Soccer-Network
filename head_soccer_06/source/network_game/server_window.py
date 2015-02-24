__author__ = 'newtonis'
import pygame
import time

from source.gui.window import Window
from source.gui.text import Text
from source.gui.button import AcceptButton,RejectButton
from source.gui.loading import LoadingAnimation
from source.data import fonts

def Round(time):
    time = float(int(time*10))/10
    return time

class ServerWindow(Window):
    def __init__(self,x,y,server_name,server_ip,parent):

        self.ip = server_ip

        Window.__init__(self,server_name,(36, 107, 97),(43, 76, 111),x,y,500,330,(255,255,255),250)
        self.parent = parent
        textIP = Text(fonts.BebasNeue.c30,server_ip,(255,255,255))
        textIP.y = 30
        textIP.x = self.width / 2 - textIP.surface.get_size()[0]/2
        self.AddElement(textIP)

        textDetails = Text(fonts.BebasNeue.c20,"DETAILS:",(255,255,255))
        textDetails.y = 70
        textDetails.x = self.width / 2 - textDetails.surface.get_size()[0]/2
        self.AddElement(textDetails)

        Mode = Text(fonts.BebasNeue.c20,"MODE:",(255,255,255))
        Mode.y = 100
        Mode.x = self.width/4 - Mode.surface.get_size()[0]/2
        self.AddElement(Mode)

        Players = Text(fonts.BebasNeue.c20,"PLAYERS:",(255,255,255))
        Players.y = 140
        Players.x = self.width/4 - Players.surface.get_size()[0]/2
        self.AddElement(Players)

        Ping = Text(fonts.BebasNeue.c20,"TCP PING:",(255,255,255))
        Ping.y = 180
        Ping.x = self.width/4 - Ping.surface.get_size()[0]/2
        self.AddElement(Ping)

        PingUDP = Text(fonts.BebasNeue.c20,"UDP PING:",(255,255,255))
        PingUDP.y = 200
        PingUDP.x = self.width/4- PingUDP.surface.get_size()[0]/2
        self.AddElement(PingUDP)

        ModeContent = Text(fonts.BebasNeue.c20,"NN",(255,255,255))
        ModeContent.y = 100
        ModeContent.x = self.width*3/4 - ModeContent.surface.get_size()[0]/2
        self.AddElement(ModeContent,"ModeShown")

        PlayersContent = Text(fonts.BebasNeue.c20,"NN",(255,255,255))
        PlayersContent.y = 140
        PlayersContent.x = self.width*3/4 - PlayersContent.surface.get_size()[0]/2
        self.AddElement(PlayersContent,"PlayersShown")

        PingContent = Text(fonts.BebasNeue.c20,"NN",(255,255,255))
        PingContent.y = 180
        PingContent.x = self.width*3/4 - PingContent.surface.get_size()[0]/2
        self.AddElement(PingContent,"PingShown")

        PingUDPcontent = Text(fonts.BebasNeue.c20,"NN",(255,255,255))
        PingUDPcontent.y = 200
        PingUDPcontent.x = self.width/4*3 - PingUDPcontent.surface.get_size()[0]/2
        self.AddElement(PingUDPcontent,"PingUDP")

        self.status = "reject"
        ##### LOADING ####

        loadingText = Text(fonts.BebasNeue.c15,"Connecting...",(255,255,255))
        loadingText.y = 230
        loadingText.x = self.width/2-loadingText.surface.get_size()[0]/2
        self.AddElement(loadingText,"LoadingText")

        loadingA = LoadingAnimation(squares=4)
        loadingA.y = 250
        loadingA.x = self.width/2-loadingA.width/2
        self.AddElement(loadingA,"LoadingA")

        ##### BUTTON REJECT #####
        rejectButton = RejectButton("Cancel")
        rejectButton.y = 290
        rejectButton.x = self.width/2 - rejectButton.imageA.get_size()[0]/2
        self.AddElement(rejectButton,"Reject")

        ##### NETWORK #####

        self.parent.SetErrorDef(self.Network_error)
        self.parent.SetConnectDef(self.Network_connected)
        self.parent.SetRBasicDef(self.Network_RBasic)
        self.parent.SetUDPsignalDef(self.UDPsignal)
        self.allowConnect = False
        self.Connect()
    def AddAcceptReject(self):
        self.status = "accept-reject"
        self.DeleteElement("Reject")

        ##### BUTTON ACCEPT #####
        acceptButton = AcceptButton("Proceed")
        acceptButton.y = 290
        acceptButton.x = self.width*3/4 - acceptButton.imageA.get_size()[0]/2
        self.AddElement(acceptButton,"Accept")

        ##### BUTTON REJECT #####
        rejectButton = RejectButton("Cancel")
        rejectButton.y = 290
        rejectButton.x = self.width/4 - rejectButton.imageA.get_size()[0]/2
        self.AddElement(rejectButton,"Reject")
    def ExtraLogicUpdate(self):
        keys = pygame.key.get_pressed()
        if self.status == "accept-reject":
            if self.references["Accept"].pressed or keys[pygame.K_RETURN]:
                self.Play()
            elif self.references["Reject"].pressed or keys[pygame.K_ESCAPE]:
                self.Quit()
        elif self.status == "reject":
            if self.references["Reject"].pressed or keys[pygame.K_ESCAPE]:
                self.Quit()
    def Quit(self):
        self.parent.locked = False
        self.parent.Kill(self)
        self.parent.CloseNetwork()
    def SetMessage(self,msj):
        self.DeleteElement("LoadingText")
        loadingText = Text(fonts.BebasNeue.c15,str(msj),(255,255,255))
        loadingText.y = 240
        loadingText.x = self.width/2-loadingText.surface.get_size()[0]/2
        self.AddElement(loadingText,"LoadingText")
    def UDPsignal(self):
        self.DeleteElement("PingUDP")
        PingUDPcontent = Text(fonts.BebasNeue.c20,str(Round(time.time()*1000 - self.count)) + "ms",(255,255,255))
        PingUDPcontent.y = 200
        PingUDPcontent.x = self.width/4*3 - PingUDPcontent.surface.get_size()[0]/2
        self.AddElement(PingUDPcontent,"PingUDP")
        if self.allowConnect:
            self.AddAcceptReject()
    def SetData(self,ping,mode,players):

        #### PING ####
        self.DeleteElement("PingShown")
        PingContent = Text(fonts.BebasNeue.c20,ping,(255,255,255))
        PingContent.y = 180
        PingContent.x = self.width*3/4 - PingContent.surface.get_size()[0]/2
        self.AddElement(PingContent,"PingShown")

        #### MODE ####
        self.DeleteElement("ModeShown")
        ModeContent = Text(fonts.BebasNeue.c20,mode,(255,255,255))
        ModeContent.y = 100
        ModeContent.x = self.width*3/4 - ModeContent.surface.get_size()[0]/2
        self.AddElement(ModeContent,"ModeShown")

        #### PLAYERS ####
        self.DeleteElement("PlayersShown")
        PlayersContent = Text(fonts.BebasNeue.c20,players,(255,255,255))
        PlayersContent.y = 140
        PlayersContent.x = self.width*3/4 - PlayersContent.surface.get_size()[0]/2
        self.AddElement(PlayersContent,"PlayersShown")

    ##### NETWORK #####


    def Connect(self):
        self.parent.TryConnection(self.ip,9999)
    def Network_error(self,data):
        self.SetMessage(data)
        self.DeleteElement("LoadingA")
        self.DeleteElement("Reject")
        rejectButton = RejectButton("Exit")
        rejectButton.y = 290
        rejectButton.x = self.width/2 - rejectButton.imageA.get_size()[0]/2
        self.AddElement(rejectButton,"Reject")
    def Network_connected(self,data):
        self.SetMessage("Requesting information")
        self.RequestData()

    def Network_RBasic(self,data):
        self.DeleteElement("LoadingA")
        ping = str( Round(time.time()*1000 - self.count) )  + " ms"
        self.SetData(ping,data["info"]["mode"],str(data["info"]["players"]) + "/" + str(data["info"]["max-players"]))
        if data["info"]["allow"]:
            print "Waiting for UDP answer..."
            self.count = time.time()*1000
            self.SendUDP({"action":"request_basicUDP"})

            self.allowConnect = True
            #self.SetMessage("Connect to server?")
            #self.AddAcceptReject()
        else:
            self.allowConnect = False
            self.SetMessage(data["info"]["reason"])

    def RequestData(self):
        self.count = time.time() * 1000
        self.Send({"action":"request_basic"})
    def Send(self,data):
        self.parent.Send(data)
    def SendUDP(self,data):
        self.parent.SendUDP(data)
    def Play(self):
        self.parent.DecideToPlay(self.title)