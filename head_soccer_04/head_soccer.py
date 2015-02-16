from PodSixNet.Connection import connection, ConnectionListener
from PodSixNet.ClientUDP import ClientUDP

import game_gg
from pgu.gui import *
from pygame.locals import *

import fonts

#gui 11 ,5

def GenerateMsj(message):
    return fonts.GetFont("VOM_35").render(message,1,(0,0,0))

class Msj:
    def __init__(self):
        self.queueMessages = []
        self.shownMessages = []
        self.position = 0,0
        self.speed = 5
        self.width = 600
        self.screen = None
    def SetTargetScreen(self,screen):
        self.targetScreen = screen
    def AddMessage(self,message):
        self.queueMessages.append(message)
    def Loop(self):
        if len(self.queueMessages) > 0:
            if len(shownMessages) == 0:
	        self.NextMessage()
            else:
                if self.shownMessages[0]["position"] > self.width/2:
                    self.NextMessage()
        for msjx in range(len(self.shownMessages)):
            msj = self.shownMessages[msjx]
            msj["position"] += self.speed
            if msj["position"] > self.width:
                del self.shownMessages[msjx]
    def NextMessage(self):
        self.shownMessages.append({"msg":self.queueMessages[0],"position":0,"image":GenerateMsj(self.queueMessages[0])})
        del self.queueMessages[0]
    def Draw(self):
        if self.targetScreen == None:
            return
        self.width = self.targetScreen.get_size()[0]
        my_surface = pygame.surface.Surface((self.targetScreen.get_size()[0],40))
        my_surface.fill((255,255,0))
	for msj in self.shownMessages:
            my_surface.blit(msj["image"],(msj["position"],20-msj["image"].get_size()[1]/2))

class RoomTable(container.Container):
    def __init__(self):
        container.Container.__init__(self)
        self.tr()
	self.td(w=Label("HOST: "))
        self.td(w=input.Input(width=200,height=20,size=20))
	
        #self.AddTextInput("input_connect",content=30)
        #self.AddContent("connect_title",input.Input(width=200,height=30,size=20,x=5,y=5))  
        
class Game(ConnectionListener):
    def __init__(self):
        self.playing = True
        self.log = []     
        self.showLogs = True
        self.showMinimalLogs = False
	self.connected = False
        self.msjer = Msj()
        self.roomTable = RoomTable()
        self.clock = pygame.time.Clock()
        self.targetScreen = None
        self.app = app.App()
        self.container = container.Container(align=-1, valign=-1)
        self.container.add(input.Input(width=200,height=20,size=20), 10, 0)
        self.app.init(self.container)
    def SetTargetScreen(self,screen):
        self.targetScreen = screen
    def tryConnection(self,host,port):
    	self.AddLog("Connecting to "+str(host)+":"+str(port),0)
        self.Connect((host,port))
    def AddLog(self,log,type):
        if self.showLogs and type == 0:
            print log
        if self.showMinimalLogs and type == 1:
            print log
        self.log.append(log)
    def Network_initial(self,data):
        pass
    def Network_message(self,data):
        self.AddLog("Server message received:"+str(data["message"]))
        self.AddMessageToQueue(data["message"])
    def AddMessageToQueue(self,message):
        self.queue_messages.append(message)
    def Draw(self):
        if self.targetScreen == None:
            return
        self.targetScreen.fill((255,255,255))
        self.app.paint()
    def Loop(self):
        self.Events()
        self.clock.tick(40)
    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            else:
                self.app.event(event)
def main():
    game   = Game()
    screen = pygame.display.set_mode((675,450),HWSURFACE|DOUBLEBUF|RESIZABLE)  
    game.SetTargetScreen(screen)
    pygame.display.set_caption("Head soccer v0.4")
    while game.playing:
        game.Draw()
        game.Loop()
        pygame.display.update()

if __name__ == "__main__":
    main()




