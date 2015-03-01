__author__ = 'grandt'
import pygame
from PodSixNet.Server import Server,Channel

class ServerChannel(Channel):
    def __init__(self , *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())
        self.ip = None
        self.conn = None
        self.console = GraphicConsole()
    def Network_print(self,data):
        self.console.Print(data["print"])
    def Network_set_basic(self,data):
        self.console.SetName(data["name"])
        self.console.SetTitleColor(data["title color"])
        self.console.SetColor(data["color"])
    def LogicUpdate(self):
        self.console.LogicUpdate()
    def GraphicUpdate(self,screen):
        self.console.GraphicUpdate(screen)

class GraphicConsole:
    def __init__(self):
        self.prints = []
        self.x,self.y = 0,0
        self.name = ""
        self.show_console = True
        self.show_title = True
        self.size = pygame.display.get_surface().get_size()[0]/2,100
        self.color = (0,0,255)
        self.title_color = (0,0,255)
        pygame.font.init()
        self.font_title = pygame.font.Font("font.ttf",30)
        self.font_text = pygame.font.Font("font.ttf",20)
    def SetName(self,name):
        self.name = name
    def SetColor(self,color):
        self.color = color
    def SetTitleColor(self,color):
        self.title_color = color
    def SetSize(self,w,h):
        self.size = w,h
    def Print(self,data):
        text = ""
        for x in data:
            text += x
            text += " "
        self.prints.append(text)
    def BlitText(self,surf):
        test_rend = self.font_text.render("HOLA",1,(0,0,0))
        y_act = self.size[1] - test_rend.get_size()[1]
        for x in self.prints:
            words = []
            temp = ""
            for y in x:
                if y == " ":
                    words.append(temp)
                    temp = ""
                else:
                    temp += y
            lines = []
            act_line = ""
            for y in words:
                act_line2 = act_line[:len(act_line)-1]
                rend = self.font_text.render(act_line2,1,(0,0,0))
                if rend.get_size()[0] > self.size[0] - 10:
                    lines.append(act_line2)
                    act_line = ""
                act_line += y + " "
            if act_line != "":
                act_line = act_line[:len(act_line)-1]
                lines.append(act_line)
            for y in lines:
                rend = self.font_text.render(y,1,(0,0,0))
                surf.blit(rend,(5,y_act))
                y_act -= rend.get_size()[1]
            y_act -= rend.get_size()[1]
    def GraphicUpdate(self,screen):
        ### Up Surface ###
        up_surface_size = 30
        up_surface = pygame.Surface((self.size[0],up_surface_size))
        up_surface.fill(self.title_color)
        title = self.font_title.render(self.name+" console",1,(0,0,0))
        up_surface.blit(title,(up_surface.get_size()[0]/2-title.get_size()[0]/2,up_surface_size/2-title.get_size()[1]/2))
        screen.blit(up_surface,(self.x,self.y))
        ### Down Surface ###
        if self.show_console:
            console = pygame.Surface(self.size)
            console.fill(self.color)
            self.BlitText(console)
            screen.blit(console,(self.x,self.y + up_surface_size))
    def LogicUpdate(self):
        pass

class Engine(Server):
    channelClass = ServerChannel
    def __init__(self):
        self.ip,self.port = "localhost",9998
        self.id = 0
        self.clients = dict()
        Server.__init__(self,localaddr=(self.ip,self.port))

    def Connected(self,channel,addr):
        print "User connected with IP",addr[0]
        channel.ip = addr[0]
        channel.conn = addr[1]
        self.clients[channel.ip] = channel
    def GraphicUpdate(self,screen):
        for x in self.clients.keys():
            self.clients[x].GraphicUpdate(screen)
    def LogicUpdate(self):
        self.Pump()
        for x in self.clients.keys():
            self.clients[x].LogicUpdate()
    def NextId(self):
        self.id += 1
        return self.id