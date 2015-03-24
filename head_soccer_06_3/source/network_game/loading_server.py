__author__ = 'newtonis'

from source.data import fonts
from source.gui.window import Window
from source.gui.loading import LoadingAnimation
from source.gui.text import Text
from source.gui.button import *
from source.gui.input import Input
from source.network_game.login import Selector
from source.database.session_query import *

class LoadingServerWindow(Window):
    def __init__(self,name,parent,onlyRooms = False):
        self.original_height = 180
        Window.__init__(self,"Welcome to "+str(name),(36, 107, 97),(43, 76, 111),0,0,500,self.original_height,(255,255,255))

        self.AddLoading()
        if onlyRooms:
            self.SetMSJ("Requesting rooms...")
        else:
            self.SetMSJ("Connecting ...")

        self.AddQuit()

        self.mode = "loading"
        parent.SetOptionRoomsDef(self.InfoReceived)
        self.mousePressed =0

    def SetOriginalHeight(self):
        self.height = self.original_height
        self.GenerateSurface()
        self.Centralize()
    def SetHeight(self,height):
        self.height = height
        self.GenerateSurface()
        self.Centralize()
    def AddLoading(self):
        loading = LoadingAnimation(1,5)
        loading.x = self.width/2-loading.width/2
        loading.y = 30
        self.AddElement(loading,"Loading")
    def RemoveLoading(self):
        self.DeleteElement("Loading")
    def RemoveMSJ(self):
        self.DeleteElement("Message")
    def AddQuit(self):
        buttonQuit = RejectButton("Cancel")
        buttonQuit.x = self.width/2-buttonQuit.imageA.get_size()[0]/2
        buttonQuit.y = 140
        self.AddElement(buttonQuit,"QUIT")
    def RemoveQuit(self):
        self.DeleteElement("QUIT")
    def SetMSJ(self,msj):
        self.DeleteElement("Message")
        message = Text(fonts.BebasNeue.c30,msj,(255,255,255))
        message.x = self.width/2-message.surface.get_size()[0]/2
        message.y = 80
        self.AddElement(message,"Message")
    def SetOpinion(self,data):
        self.mode = "opinion"
        self.RemoveLoading()
        self.RemoveMSJ()
        self.RemoveQuit()
        textQuestion = Text(fonts.BebasNeue.c25,data["content"]["question"],(255,255,255))
        textQuestion.x = self.width/2-textQuestion.surface.get_size()[0]/2
        textQuestion.y = 30
        self.AddElement(textQuestion,"Question")

        self.optionsButtons = []
        for x in range(len(data["content"]["options"])):
            button_text = data["content"]["options"][x]
            button = NeutralButton(button_text,400)
            button.x = self.width/2-button.imageA.get_size()[0]/2
            button.y = 70 + 45*x
            name = "Button "+str(x)
            self.AddElement(button,name)
            self.optionsButtons.append(name)
            if button.y > self.height:
                self.SetHeight(button.y+50)
    def SetNameInput(self,with_error = None):
        self.RemoveLoading()
        self.RemoveMSJ()
        self.RemoveQuit()
        self.RemoveLoading()
        self.RemoveMSJ()
        self.RemoveQuit()
        self.mode = "setting-name"

        y_act = 30

        if with_error != None:
            error = Text(fonts.BebasNeue.c20,with_error,(255,0,0))
            error.x = self.width/2 - error.surface.get_size()[0]/2
            error.y = y_act
            self.AddElement(error,"Error")
            y_act += error.surface.get_size()[1] + 5

        textQuestion = Text(fonts.BebasNeue.c30,"Name:",(255,255,255))
        textQuestion.x = self.width/4
        textQuestion.y = y_act
        self.AddElement(textQuestion,"Question")

        input = Input()
        input.AllowAll()
        input.SetSize(200,30)
        input.x = textQuestion.x + textQuestion.surface.get_size()[0] + 10
        input.y = y_act
        input.SetTextColor(0,0,0)
        input.SetBackgroundColor(100,100,100)
        self.AddElement(input,"Input")
        y_act += 50

        confirmButton = AcceptButton("Confirm")
        confirmButton.x = self.width/2-confirmButton.size[0]/2
        confirmButton.y = y_act
        self.AddElement(confirmButton,"Confirm")
        y_act += confirmButton.size[1]

        self.SetHeight(y_act)
    def ExtraLogicUpdate(self):
        if self.mode == "loading":
            if self.references["QUIT"].pressed and not self.mousePressed:
                self.Cancel()
        elif self.mode == "opinion":
            for buttonID in range(len(self.optionsButtons)):
                if self.references[self.optionsButtons[buttonID]].pressed:
                    self.HandleButtonPressed(buttonID)
                    break
        elif self.mode == "setting-name":
            if not self.ButtonCheck("Confirm") and self.mousePressed == 1:
                self.mousePressed = 0
            if not pygame.key.get_pressed()[pygame.K_RETURN] and self.mousePressed == 2:
                self.mousePressed = 0
            if (self.references["Confirm"].pressed or pygame.key.get_pressed()[pygame.K_RETURN]) and not self.mousePressed:
                if self.references["Confirm"].pressed:
                    self.mousePressed = 1
                else:
                    self.mousePressed = 2
                SessionDeclareGuestName(self.references["Input"].text)
                self.Send({"action":"send_name","name":self.references["Input"].text})
                self.FinalLoadingPart()
    def HandleButtonPressed(self,id):
        self.Send({"action":"get_opinion","option":id})
        for button in self.optionsButtons:
            self.DeleteElement(button)
        self.DeleteElement("Question")
        self.SetOriginalHeight()
        self.mode = "loading"
        self.AddLoading()
        self.SetMSJ("Setting your profile...")
        self.AddQuit()
    def FinalLoadingPart(self):
        self.mode = "loading"
        self.DeleteElement("Question")
        self.DeleteElement("Input")
        self.DeleteElement("Confirm")
        self.DeleteElement("Error")
        self.SetOriginalHeight()
        self.AddLoading()
        self.SetMSJ("Loading rooms ...")
        self.AddQuit()
    def Cancel(self):
        self.parent.Return2ServerList()
    def InfoReceived(self,type,data):
        if type == "opinion":
            self.SetOpinion(data)
        elif type == "rooms":
            self.Kill()
            self.parent.Go2GameList(self.title,data)
        elif type == "skip":
            self.SetMSJ("Setting your profile...")
        elif type == "req-name":
            self.parent.DeleteWindow("Loading")
            self.parent.AddWindowCenteredOnFront(Selector(self.parent,self),pygame.display.get_surface(),"Login")
        elif type == "error-name":
            self.SetNameInput(data["error"])
    def Send(self,data):
        self.parent.Send(data)