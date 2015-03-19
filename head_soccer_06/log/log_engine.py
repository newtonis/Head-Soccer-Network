__author__ = 'grandt'
import pygame
from PodSixNet.Server import Server,Channel

def AddBorder(surface,b=1,color=(0,0,0),special=True):
    if not surface.get_colorkey():
        surface.set_colorkey((0,0,1))
    width,height = surface.get_size()

    b1Surface = pygame.surface.Surface((width,b))
    b2Surface = pygame.surface.Surface((b,height))

    b1Surface.fill(color)
    b2Surface.fill(color)

    surface.blit(b1Surface,(0,0))
    surface.blit(b2Surface,(0,0))
    surface.blit(b1Surface,(0,height-b))
    surface.blit(b2Surface,(width-b,0))

    if special:
        white = pygame.surface.Surface((1,1))
        white.fill(surface.get_colorkey())
        surface.blit(white,(0,0))
        surface.blit(white,(0,height-1))
        surface.blit(white,(width-1,0))
        surface.blit(white,(width-1,height-1))

class ServerChannel(Channel):
    def __init__(self , *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())
        self.ip = None
        self.conn = None
        self.console = GraphicConsole(self)
        self.column = 0
        self.initialized = False
    def Network_print(self,data):
        self.console.Print(data["print"],data["error"])
    def Network_set_basic(self,data):
        self.console.SetName(data["name"])
        self.console.SetTitleColor(data["title color"])
        self.console.SetColor(data["color"])
        self.column = data["column"]
        while len(self._server.columns) <= self.column:
            self._server.columns.append(list())
        self.initialized = True
        self._server.columns[self.column].append(self)
        self._server.SetActive(self.id)
    def LogicUpdate(self):
        self.console.LogicUpdate()
    def GraphicUpdate(self,screen):
        self.console.GraphicUpdate(screen)
    def Close(self):
        del self._server.clients[self.id]
        for x in range(len(self._server.columns[self.column])):
            if self._server.columns[self.column][x] == self:
                del self._server.columns[self.column][x]
                break
        if len(self._server.columns[self.column]) != 0:
            self._server.SetActive(self._server.columns[self.column][len(self._server.columns[self.column])-1].id)

class GraphicConsole:
    def __init__(self,parent):
        self.parent = parent
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
        self.recently_pressed = False
    def SetName(self,name):
        self.name = name
    def SetColor(self,color):
        self.color = color
    def SetTitleColor(self,color):
        self.title_color = color
    def SetSize(self,w,h):
        self.size = w,h
    def Print(self,data,error=False):
        text = ""
        for x in data:
            text += str(x)
            text += " "
        self.prints.append({"Text":text,"Error":error})
    def BlitText(self,surf):
        test_rend = self.font_text.render("HOLA",1,(0,0,0))
        y_act = self.size[1] - test_rend.get_size()[1]
        for n in range(len(self.prints)-1,-1,-1):
            x = self.prints[n]
            words = []
            temp = ""
            for y in x["Text"]:
                if y == " ":
                    words.append(temp)
                    temp = ""
                else:
                    temp += y
            lines = []
            word_start = 0
            for y in range(len(words)):
                text = ""
                for w in range(word_start,y):
                    text += words[w] + " "
                rend = self.font_text.render(text,1,(0,0,0))
                if rend.get_size()[0] > self.size[0] - 10:
                    text = ""
                    for w in range(word_start,y-1):
                        text += words[w] + " "
                    lines.append([text,x["Error"]])
                    word_start = y - 1
            text = ""
            for y in range(word_start,len(words)):
                text += words[y] + " "
            if text != "":
                lines.append([text,x["Error"]])
            for y in range(len(lines)-1,-1,-1):
                if lines[y][1]:
                    color = (255,0,0)
                else:
                    color = (0,0,0)
                rend = self.font_text.render(lines[y][0],1,color)
                surf.blit(rend,(5,y_act))
                y_act -= rend.get_size()[1]
    def GraphicUpdate(self,screen):
        ### Up Surface ###
        up_surface_size = 30
        if self.show_title:
            up_surface = pygame.Surface((self.size[0],up_surface_size))
            up_surface.fill(self.title_color)
            AddBorder(up_surface)
            title = self.font_title.render(self.name,1,(0,0,0))
            up_surface.blit(title,(up_surface.get_size()[0]/2-title.get_size()[0]/2,up_surface_size/2-title.get_size()[1]/2))
            screen.blit(up_surface,(self.x,self.y))
        ### Down Surface ###
        if self.show_console:
            console = pygame.Surface(self.size)
            console.fill(self.color)
            AddBorder(console)
            self.BlitText(console)
            screen.blit(console,(self.x,self.y + up_surface_size))
    def LogicUpdate(self):
        x,y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if x > self.x and y > self.y and x < self.x + self.size[0] and y < self.y + 30:
                if not self.recently_pressed:
                    self.recently_pressed = True
                    self.parent._server.SetActive(self.parent.id)
        else:
            self.recently_pressed = False

class Engine(Server):
    channelClass = ServerChannel
    def __init__(self):
        self.ip,self.port = "localhost",1998
        self.id = 0
        self.clients = dict()
        self.right_last = 0
        self.left_last = 0
        self.columns = []
        self.columns_active = dict()
        Server.__init__(self,localaddr=(self.ip,self.port))
    def Connected(self,channel,addr):
        print "User connected with IP",addr[0]
        channel.ip = addr[0]
        channel.conn = addr[1]
        self.clients[channel.id] = channel
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
    def SetActive(self,id,recusion = False):
        if self.clients.has_key(id):
            if self.clients[id].initialized:
                position = -1
                client =  self.clients[id]
                column = client.column
                if not recusion:
                    self.columns_active[column] = id
                    for x in range(len(self.columns)):
                        if x != column:
                            if self.columns_active.has_key(x):
                                self.SetActive(self.columns_active[x],True)
                for y in range(len(self.columns[column])):
                    if self.columns[column][y] == self.clients[id]:
                        position = y
                y_act = 0
                surf_size = 600-30*len(self.columns[column])
                x_pos = (900/len(self.columns))*column
                for y in range(len(self.columns[column])):
                    self.columns[column][y].console.x = x_pos
                    self.columns[column][y].console.y = y_act
                    self.columns[column][y].console.size = [900.0/len(self.columns),surf_size]
                    if y != position:
                        self.columns[column][y].console.show_console = False
                    else:
                        client.console.show_console = True
                        y_act += surf_size
                    y_act += 30