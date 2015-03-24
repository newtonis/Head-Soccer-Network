__author__ = 'ariel'
import pygame #the graphics library
import time #time utilities

from source.gui.graphicManager import GraphicManager #the client game admin
from source.gui.mouseIcon import * #change mouse icon utilites
from random import randrange
from log.log_client import Log

def main():
    screen = pygame.display.set_mode((900,600),pygame.HWSURFACE) #create the game window
    pygame.display.set_caption("Head soccer 06")
    graphicManager = GraphicManager() #instanciate the graphic manageManager.StartNetworkGame() #tell graphic manager to start network game
    graphicManager.SetScreen(screen)
    graphicManager.StartNetworkGame()
    clock = pygame.time.Clock() #to handle fps
    Log.SetBasic("Client console",(0,124,255),(0,224,255),1) #log console
    continuar = True
    while continuar: #while the game is running
        if 1:
            events = pygame.event.get()
            graphicManager.Event(events)
            for event in events:
                if event.type == pygame.QUIT or graphicManager.endSignal == 1:
                    continuar = False
                    #server_run.server.play = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            continuar = False
                    if event.key == pygame.K_s and pygame.key.get_pressed()[pygame.K_LSHIFT]: #to take a screenshot
                        print "screenshot mode"
                        file = raw_input("filename:")
                        if file != "cancel":
                            pygame.image.save(screen,"extras/screenshots/"+file)
                        else:
                            print "screenshot canceled"
            if int(time.time()) % 60*30 == 0:
                try:
                    pygame.image.save(screen,"extras/creenshots/auto/"+"auto_"+str(int(time.time()))+"_"+str(randrange(1000))+".png")
                except:
                    pass
            screen.fill((100,100,100))
            graphicManager.LogicUpdate() #logic working
            graphicManager.GraphicUpdate(screen) #paiting the game in the screen
            Log.LogicUpdate()
            updateCursor()
            clock.tick(40) #we'll play with 40 fps
        #except IndexError as inst:
        #    Log.PrintError(inst)

    graphicManager.End()
if __name__ == "__main__":
    main()