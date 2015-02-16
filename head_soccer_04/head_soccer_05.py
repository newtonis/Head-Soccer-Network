
#logs
from logs import *

#pygame
import pygame

#PodSixNet imports
from PodSixNet.Connection import connection, ConnectionListener
from PodSixNet.ClientUDP import ClientUDP

#pgu imports
from pgu.gui import *

#for global access
access = dict()
    
class Network(ConnectionListener):
    def __init__(self):
        pass

class Game(Log_object):
    def __init__(self,ratio = 1):
        Log_object.__init__(self)  
        self.AddCritical("Starting game...") 
        self.playing = True
        self.UpdateScreenSize(900*ratio,600*ratio)
        self.state = "2connect"
	self.current_area = Connecting_area()
        self.clock = pygame.time.Clock()
        self.freq  = 40
    def UpdateScreenSize(self,width,height):
        self.AddCritical("Resizing "+str(int(width))+"x"+str(int(height)) )
        global access
        access["screen"] = pygame.display.set_mode((int(width),int(height)))
        access["screen-width"],access["screen-height"] = access["screen"].get_size()
        self.screen = access["screen"]
    def Draw(self):
        self.screen.fill((255,255,255))
        self.current_area.Draw()
        pygame.display.update() 
    def Loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            self.current_area.Event(event)
        self.Draw()
        self.clock.tick(self.freq)
    def Run(self):
        self.AddCritical("Starting loop...")
        while self.playing:
            self.Loop()

class Connecting_menu:
    def __init__(self):
        self.container   = container.Container(align=0,valign=-1,borderColor=(0,0,0))
        self.tableUpArea = table.Table()
        self.tableUpArea.tr()
        self.tableUpArea.td(w=Label("HOST: ",color=(0,0,255)))
        self.tableUpArea.td(w=Input("Here"))
        self.container.add(self.tableUpArea,0,10)
    def DrawBackound(self):
        global access
        access["screen"].blit(self.backgroundSurface())
class Connecting_area:
    def __init__(self):
        self.app          = app.App() #pgu app
      	self.menu = Connecting_menu()
        self.app.init(self.menu.container)
        
    def Draw(self):
        self.app.paint()
        self.menu.DrawBackground()
    def Event(self,event):
        self.app.event(event)
class Gaming:
    def __init__(self):
        pass

def main():
    access["game"]    = Game(0.75)
    access["Network"] = Network()
    access["game"].Run()

if __name__ == "__main__":
    main()


