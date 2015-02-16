__author__ = 'Dylan'
import pygame
from source.gui.window import Window
from source.gui.text import Text
from source.data.fonts import BebasNeue
from source.gui.input import Input
from source.gui.button import AcceptButton,RejectButton
from source.database import serverQ

class AddServer(Window):
    def __init__(self,parent):
        self.parent = parent

        Window.__init__(self, "Add server", (36, 107, 97), (43, 76, 111), 0, 0, 500, 250, (255,255,255), 250)
        y_act = 40 + 5
        name = Text(BebasNeue.c30,"Server name",(0,0,0))
        name.x = self.width/4 - name.surface.get_size()[0]/2
        name.y = y_act
        self.AddElement(name,"Name")
        #y_act += 3+name.surface.get_size()[1]

        name_input = Input()
        name_input.AllowAll()
        name_input.SetSize(200,30)
        name_input.x = self.width/4*3 - name_input.size[0]/2
        name_input.y = y_act
        name_input.SetTextColor(255,0,0)
        name_input.SetBackgroundColor(100,100,100)
        self.AddElement(name_input,"Name input")
        y_act += name_input.size[1]+name_input.border_size*2+10

        ip = Text(BebasNeue.c30,"IP Adress",(0,0,0))
        ip.x = self.width/4 - ip.surface.get_size()[0]/2
        ip.y = y_act
        self.AddElement(ip,"IP")
        #y_act += ip.surface.get_size()[1]+3

        ip_input = Input()
        ip_input.AllowNumbers()
        ip_input.SetSize(200,30)
        ip_input.x = self.width/4*3 - ip_input.size[0]/2
        ip_input.y = y_act
        ip_input.SetTextColor(255,0,0)
        ip_input.SetBackgroundColor(100,100,100)
        name_input.SetNextInput(ip_input)
        self.AddElement(ip_input,"IP input")
        y_act += ip_input.size[1]+2*ip_input.border_size+15

        accept_button = AcceptButton("Create",150,[self.width/2+20,y_act])
        self.AddElement(accept_button,"Create button")

        cancel_button = RejectButton("Cancel",150,[self.width/2-150-20,y_act])
        self.AddElement(cancel_button,"Cancel button")

        y_act += cancel_button.size[1]+5

        self.height = y_act
        self.GenerateSurface()
        self.tab = False
        self.tab_elements = ["Name input","IP input"]
        self.current_tab = -1
    def Exit(self):
        self.parent.locked = False
        self.parent.Kill(self)
    def ExtraLogicUpdate(self):
        if self.references["Cancel button"].pressed:
            self.Exit()
        pressed = pygame.key.get_pressed()
        if self.references["Create button"].pressed or pressed[pygame.K_RETURN]:
            serverQ.AddServer(self.references["IP input"].text,self.references["Name input"].text)
            self.parent.references["Server List"].UpdateLocalServers()
            self.Exit()
        if not pressed[pygame.K_TAB]:
            self.tab = False