__author__ = 'ariel'

from source.database import session_query
from source.data import fonts
from source.gui.text import Text
from source.gui.window import Window
from source.gui.button import *
from source.gui.loading import LoadingAnimation
from source.gui.input import Input

class CheckReopenWindow(Window):
    def __init__(self,parent,dataSession):
        Window.__init__(self,"Restore game",(253,245,230),(30,144,255),0,0,400,330,(0,0,0),255,(0,0,0))
        self.parent = parent
        self.data = dataSession

        textColor = 255,255,255
        title = Text(fonts.BebasNeue.c15,"Your last connection data:",textColor)
        title.x = self.width/2 - title.surface.get_size()[0]/2
        title.y = 30
        self.AddElement(title,"Tittle")

        if dataSession["status"] == "TryConnect" or dataSession["status"] == "TryConnectRoom":
            server = Text(fonts.BebasNeue.c20,"Server Address: ",textColor);
            server.x = self.width / 4 - server.surface.get_size()[0]/2
            server.y = 80 - server.surface.get_size()[1]/2
            self.AddElement(server,"Server title")

            server_IP = Text(fonts.BebasNeue.c30,str(dataSession["ip"]),textColor)
            server_IP.x = self.width / 4 * 3 - server_IP.surface.get_size()[0]/2
            server_IP.y = 80 - server_IP.surface.get_size()[1]/2
            self.AddElement(server_IP,"ip data")

            if dataSession["logData"]["type"] == "needGuestName":
                textInfo = Text(fonts.BebasNeue.c30,"You need to be asigned a name!",textColor)
                textInfo.x = self.width / 2 - textInfo.surface.get_size()[0]/2
                textInfo.y = 90 - textInfo.surface.get_size()[1]/2
                self.AddElement(textInfo,"textInfo")
            else:
                textSession = Text(fonts.BebasNeue.c15,"Your login data:",textColor)
                textSession.x = self.width / 2 - textSession.surface.get_size()[0]/2
                textSession.y = 130 - textSession.surface.get_size()[1]/2
                self.AddElement(textSession,"sessionData")

                textType = Text(fonts.BebasNeue.c20,"Type:",textColor)
                textType.x = self.width / 4 - textType.surface.get_size()[0]/2
                textType.y = 160 - textSession.surface.get_size()[1]/2
                self.AddElement(textType,"sessionTypeText")



                if dataSession["logData"]["type"] == "guest":
                    textContentType = Text(fonts.BebasNeue.c30,"Guest",textColor)
                else:
                    textContentType = Text(fonts.BebasNeue.c20,"Login",textColor)

                    ### ADD PASSWORD FIELD
                    passTitle = Text(fonts.BebasNeue.c20,"password:",textColor)
                    passTitle.y = 220 - passTitle.surface.get_size()[1]/2
                    passTitle.x = self.width / 4 - passTitle.surface.get_size()[0]/2
                    self.AddElement(passTitle,"passTitle")

                    passContent = Text(fonts.BebasNeue.c30,"****",textColor)
                    passContent.y = 225 - passContent.surface.get_size()[1]/2
                    passContent.x = self.width / 4 * 3 - passContent.surface.get_size()[0]/2
                    self.AddElement(passContent,"passContent")

                titleName = Text(fonts.BebasNeue.c20,"User:",textColor)
                titleName.x = self.width / 4 - titleName.surface.get_size()[0]/2
                titleName.y = 200 - titleName.surface.get_size()[1]/2
                self.AddElement(titleName,"titleName")


                nameContent = Text(fonts.BebasNeue.c20,dataSession["logData"]["name"],textColor)
                nameContent.x = self.width / 4 * 3 - nameContent.surface.get_size()[0]/2
                nameContent.y = 200 - nameContent.surface.get_size()[1]/2
                self.AddElement(nameContent,"name")


                ### ADD TEXT CONTENT TYPE, GUEST OR LOGIN

                textContentType.x = self.width/4*3 - textContentType.surface.get_size()[0]/2
                textContentType.y = 160 - textContentType.surface.get_size()[1]/2
                self.AddElement(textContentType,"contentType")

                if dataSession["status"] == "TryConnectRoom":
                    titleRoom = Text(fonts.BebasNeue.c20,"Room",textColor)
                    titleRoom.x = self.width / 4 - titleRoom.surface.get_size()[0]/2
                    titleRoom.y = 240 - titleRoom.surface.get_size()[1]/2
                    self.AddElement(titleRoom,"titleRoom")

                    roomContent = Text(fonts.BebasNeue.c20,dataSession["room"],textColor)
                    roomContent.x = self.width / 4 * 3 - roomContent.surface.get_size()[0]/2
                    roomContent.y = 240 - roomContent.surface.get_size()[1]/2
                    self.AddElement(roomContent,"roomName")
                self.AddButtons()
        self.parent.SetOptionRoomsDef(self.JoiningActions)
        self.parent.SetErrorDef(self.Network_Error)
        self.parent.SetConnectDef(self.Network_connected)
        self.parent.SetRBasicDef(self.Network_RBasic)
        self.parent.SetLoginDef(self.LoginSuccess)
    def AddButtons(self):
        buttonCancel = RejectButton("Cancel",150)
        buttonCancel.x = self.width / 4 - buttonCancel.imageA.get_size()[0]/2
        buttonCancel.y = 290
        self.AddElement(buttonCancel,"Cancel")

        buttonAccept = AcceptButton("Restore",150)
        buttonAccept.x = self.width / 4 * 3 - buttonAccept.imageA.get_size()[0]/2
        buttonAccept.y = 290
        self.AddElement(buttonAccept,"Accept")
    def AddEndButton(self):
        buttonEnd = NeutralButton("OK",150)
        buttonEnd.x = self.width / 2 - buttonEnd.imageA.get_size()[0]/2
        buttonEnd.y = self.width - 70
        self.AddElement(buttonEnd,"Cancel")
    def LogicUpdate(self):
        Window.LogicUpdate(self)

        if self.ButtonCheck("Cancel"):
            self.Kill()
            session_query.SessionDeclareDisconnect()
        elif self.ButtonCheck("Accept"):
            self.RestoreSession(self.data)
        elif self.ButtonCheck("okButton"):
            self.SendName(self.references["inputField"].text)
    def LoadingMode(self):
        self.DeleteAllElements()
        self.SetHeight(170)
        self.SetMSJ("Connecting to "+self.ip+" ...")
        self.SetLoadingAnimation()
    def SetMSJ(self,msj):
        self.DeleteElement("MSJ_loading")
        msjLoading = Text(fonts.BebasNeue.c25,msj,(255,255,255))
        msjLoading.y = 100
        msjLoading.x = self.width / 2 - msjLoading.surface.get_size()[0] / 2
        self.AddElement(msjLoading,"MSJ_loading")
    def SetLoadingAnimation(self):
        self.DeleteElement("ANI_loading")
        animation = LoadingAnimation()
        animation.y = 50
        animation.x = self.width / 2 - animation.width/2
        self.AddElement(animation,"ANI_loading")
    def SetNoConnectMSJ(self):
        self.DeleteAllElements()
        self.SetHeight(170)
        self.SetMSJ("Could not connect to server")
        self.AddEndButton()
    def NotAllowed(self,data):
        self.SetMSJ(data["reason"])
        self.AddEnddButton()
    def SetInputName(self):
        self.DeleteAllElements()
        nameInputTitle = Text(fonts.BebasNeue.c30,"Name:",(255,255,255))
        nameInputTitle.y = 100 - nameInputTitle.surface.get_size()[1]/2
        nameInputTitle.x = self.width / 4 - nameInputTitle.surface.get_size()[0]/2
        self.AddElement(nameInputTitle,"nameInput")

        inputField = Input()
        inputField.SetSize(150,30)
        inputField.y = 100 - inputField.size[1]/2
        inputField.x = self.width / 4 * 3 - inputField.size[0]/2
        inputField.AllowAll()
        self.AddElement(inputField,"inputField")

        okButton = AcceptButton("Accept",200)
        okButton.y = 150 - okButton.size[1]/2
        okButton.x = self.width/ 2 - okButton.imageA.get_size()[0]/2
        self.AddElement(okButton,"okButton")

    def RemoveInputName(self):
        self.DeleteElement("nameInput")
        self.DeleteElement("inputField")
        self.DeleteElement("inputError")
        self.DeleteElement("okButton")
    def AddInputError(self,error):
        text = Text(fonts.BebasNeue.c20,"Sorry, your name is being used in this server",(200,0,0))
        text.y = 50
        text.x = self.width / 2 - text.surface.get_size()[0] / 2
        self.AddElement(text,"inputError")
    def RestoreSession(self,data): ### try to rejoin previous game ###
        print "Restoring session with data ",data
        if data["status"] == "NoConnect":
            print "Data don't own any ip address"
            return
        self.ip = data["ip"]

        self.LoadingMode()
        self.parent.TryConnection(data["ip"],9999)

    def Network_connected(self,data):
        print "Connection enablished with the reopen window"
        self.Send({"action":"request_basic"})
        self.parent.DeleteWindow("Server List")
    def Network_RBasic(self,data):
        print "Basic data arrived",data
        if not data["info"]["allow"]:
            self.NotAllowed(data)
            return
        self.serverData = data["info"]
        self.RequestRooms()

    def RequestRooms(self):
        self.SetMSJ("Requesting rooms ...")
        self.Send({"action":"request_rooms"})
    def Authenticate(self):
        if self.data["logData"]["type"] == "guest":
            self.Send({"action":"send_name","name":self.data["logData"]["name"]})
            self.SetMSJ("Joining as guest '"+self.data["logData"]["name"]+"'")
        elif self.data["logData"]["type"] == "login":
            self.Send({"action":"check_login","username":self.data["logData"]["name"],"password":self.data["logData"]["pass"]})
            self.SetMSJ("Logging as '"+self.data["logData"]["name"]+"'")
    def Network_Error(self,data):
        self.SetNoConnectMSJ()
    def JoiningActions(self,type,data):
        if type == "req-name":
            self.Authenticate()
        elif type == "rooms":
            if self.data["status"] == "TryConnect":
                self.parent.Go2GameList(self.serverData["name"],data)
            elif self.data["status"] == "TryConnectRoom":
                self.Send({"action":"join_game","room_name":self.data["room"]})
            self.Kill()
        elif type == "error-name":
            print "Name already taken"
            self.SetInputName()
            self.AddInputError("Name already taken")
    def LoginSuccess(self,data):
        print "Login successful",data
    def SendName(self,value):
        self.Send({"action":"send_name","name":value})
        self.RemoveInputName()
        self.SetLoadingAnimation()
        self.SetMSJ("Setting name ...")
    def Send(self,data):
        self.parent.Send(data)
