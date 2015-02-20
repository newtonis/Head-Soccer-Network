__author__ = 'ariel'
import pygame #the graphics library
import time #time utilities

from source.gui.graphicManager import GraphicManager #the client game admin
from source.gui.mouseIcon import * #change mouse icon utilites

import threading #not needed actually
import server_run #not needed actually
from random import randrange

def main():
    #serverTh = threading.Thread(target=server_run.main,name="Server thread")
    #serverTh.start()hacemos dos uno
    screen = pygame.display.set_mode((900,600),pygame.RESIZABLE) #create the game window
    pygame.display.set_caption("Head soccer 06")
    graphicManager = GraphicManager() #instanciate the graphic manageManager.StartNetworkGame() #tell graphic manager to start network game
    graphicManager.SetScreen(screen)
    graphicManager.StartNetworkGame()
    clock = pygame.time.Clock() #to handle fps
    continuar = True
    while continuar: #while the game is running
        events = pygame.event.get()
        graphicManager.Event(events)
        for event in events:
            if event.type == pygame.QUIT:
                continuar = False
                #server_run.server.play = False
            elif event.type == pygame.KEYDOWN:
                pass
                if event.key == pygame.K_s and pygame.key.get_pressed()[pygame.K_LSHIFT]: #to take a screenshot
                    print "screenshot mode"
                    file = raw_input("filename:")
                    if file != "cancel":
                        pygame.image.save(screen,"screenshots/"+file)
                    else:
                        print "screenshot canceled"
            #elif event.type == pygame.VIDEORESIZE:
             #   screen = pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)
        #if int(time.time()) % 60 == 0:
        #    pygame.image.save(screen,"screenshots/auto/"+"auto_"+str(int(time.time()))+"_"+str(randrange(1000))+".png")
        screen.fill((100,100,100))
        graphicManager.LogicUpdate() #logic working
        graphicManager.GraphicUpdate(screen) #paiting the game in the screen
        updateCursor()
        clock.tick(40) #we'll play with 40 fps
        #pygame.display.update()

    clock.tick(20)
    graphicManager.End()
if __name__ == "__main__":
    main()