import pygame

from source.gui.window import Window
from source.gui.text import Text
from source.gui.button import AdvancedButton,Button,ButtonImage,BUTTON_IMAGES,ClassicButton
from source.data import fonts
from source.network_game import list_system
from source.network_game.server_window import ServerWindow
from source.database.mysql import MySQL

import source.network_game.add_server_window as AddServerWindow

def add0(value):
    if value < 10:
        return "00"+str(value)
    if value < 100:
        return "0"+str(value)
    return str(value)

class ServerListWindow(Window):
    def __init__(self):
        ww,hh = pygame.display.get_surface().get_size()
        ww -= 50
        hh -= 50
        Window.__init__(self,"MULTITPLAYER GAME",(36, 107, 97),(43, 76, 111),0,0,ww,hh,(255,255,255))
        self.enabled = False
        self.locked = True

        title = Text(fonts.BebasNeue.c40,"SERVER BROWSER",(255,255,255))
        title.x = self.width/2-title.surface.get_size()[0]/2
        title.y = 35
        self.AddElement(title)

        #bar = Bar(10,400,0.1,self.width-50,100)
        #self.AddElement(bar)
        listSystem = list_system.ListSystem(0,0,True,self.height-250)
        listSystem.AddUpKey("Name",400)
        listSystem.AddUpKey("IP",150)
        listSystem.AddUpKey("Mode",150)
        listSystem.y = 100
        listSystem.x = self.width/2-listSystem.width/2
        self.AddElement(listSystem,"ListSystem")

        connectButton = AdvancedButton((350,80),(0,0),"Connect",(63,20,57),(43,11,39))
        distance_to_back_list = (listSystem.y + 70 + listSystem.height)
        connectButton.y = (self.height - distance_to_back_list)/2 + distance_to_back_list - connectButton.image.get_size()[1]/2
        connectButton.x = self.width/2 - connectButton.image.get_size()[0]/2
        self.AddElement(connectButton,"ConnectButton")

        """add = ClassicButton("+",(0,255,0),(0, listSystem.y + listSystem.height + 50))
        add.x = listSystem.x + listSystem.width - add.imageA.get_size()[0]
        self.AddElement(add,"AddButton")

        remove = ClassicButton("-",(255,0,0),(0,add.y))
        remove.x = add.x - remove.size[0]
        self.AddElement(remove,"RemoveButton")"""

        self.LoadLocalSevers()
    def AddFake(self):
        for x in range(20):
            self.AddRow(add0(x)+":"+add0(x)+":"+add0(x)+":"+add0(x),"fake server "+str(x))
    def LoadLocalSevers(self):
        MySQL.CheckDeadServers()
        for row in MySQL.GetServers():
            self.AddRow(row["IP"],row["Name"])
    def UpdateLocalServers(self):
        self.references["ListSystem"].contents = []
        self.LoadLocalSevers()
    def AddRow(self,ip,name):
        self.references["ListSystem"].AddRow({"IP":ip,"Name":name,"Mode":"NN"})
    def ExtraLogicUpdate(self):
        if not self.enabled:
            return
        if self.references["ConnectButton"].pressed or pygame.key.get_pressed()[pygame.K_RETURN]:
            if self.references["ListSystem"].selected != -1:
                self.HandleServerWindowOpen(self.references["ListSystem"].ServerOpen())
                self.enabled = False

        """if self.references["AddButton"].pressed:
            self.AddServer()
            self.enabled = False
        if self.references["RemoveButton"].pressed:
            if self.references["ListSystem"].selected != -1:
                serverQ.DeleteServer(self.references["ListSystem"].contents[self.references["ListSystem"].selected].content["Name"])
                self.UpdateLocalServers()
                self.references["ListSystem"].selected = -1"""

    def HandleServerWindowOpen(self,server):
        self.parent.AddWindowCenteredOnFront(ServerWindow(0,0,server["Name"],server["IP"],self.parent),pygame.display.get_surface())
    def AddServer(self):
        self.parent.AddWindowCenteredOnFront(AddServerWindow.AddServer(self.parent),pygame.display.get_surface())