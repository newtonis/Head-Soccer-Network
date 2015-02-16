from order_update_list import *

import pygame
import time

pygame.font.init()
basic_font = pygame.font.Font(None,20)

def GCP(surfaceA,surfaceB):
     return surfaceA.get_size()[0]/2-surfaceB.get_size()[0]/2 , surfaceB.get_size()[1]/2 - surfaceB.get_size()[1]/2
def GN(number):
     if number == 1:
         return ""
     else:
         return " #"+str(number)
def AddBorder(surface):
     w,h = surface.get_size()
     pygame.draw.lines(surface,(0,0,0),0,[(0,0),(w-1,0),(w-1,h-1),(0,h-1)])
    
class WW(OrderUpdateList,OULelement): #Window
     def __init__(self,upcolor,centercolor,dimensions=(300,200),screen = None,title="default"):
         OrderUpdateList.__init__(self,screen)
         self.upcolor     = upcolor
         self.centercolor = centercolor
         self.dimensions   = dimensions
         self.SetScreen(screen)
         self.x,self.y = 0,0
         self.Center()
         self.title = title
         self.GenerateSurface()
         
     def SetTitle(self,title):
         self.title = title
         self.GenerateSurface()
     def Center(self):
         if self.screen != None:
             self.x , self.y =  GCP(self.screen,self.dimensions)
     def extraDraw(self):
         self.screen.blit(self.backgroundSurface,(self.x,self.y))
     def GenerateSurface(self):
         self.backgroundSurface = pygame.surface.Surface((self.dimensions[0],self.dimensions[1] + 24))
         upSurface   = pygame.surface.Surface((self.dimensions[0],25))
	 upSurface.fill(self.upcolor) 
         AddBorder(upSurface)
         downSurface = pygame.surface.Surface(self.dimensions)
         downSurface.fill(self.centercolor)
         AddBorder(downSurface) 
         
         imageTextSurface = basic_font.render(self.title,0,(0,0,0)) 
         upSurface.blit(imageTextSurface,Center(upSurfae,imageTextSurfae ))
         self.backgroundSurface.blit(upSurface,(0,0))
         self.backgroundSurface.blit(downSurface,(0,24))
class BasicWindow(WW):
     def __init__(self):
         WW.__init__(self, upcolor=(0,94,124),centercolor=(94,249,43))
class Game(OrderUpdateList,OULelement):
     def __init__(self,screen):
         OrderUpdateList.__init__(self,screen)
     def AddFrontWindow(self,window,title):
         window.SetTitle(title)
         self.AddElement(window,title)


def main():
     screen = pygame.display.set_mode((900,675))
     continuar = True
     g = Game(screen)
     g.AddFrontWindow(BasicWindow(),"Basic window")

     lUpdate = time.time()
     clock   = pygame.time.Clock()
    
     while continuar:
          screen.fill((255,255,255))
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                   continuar = False
              else:
                   g.Event(event)

          time_passed = time.time() - lUpdate
          lUpdate     = time.time()
          g.UTimes(time_passed)
          g.Draw()         
          pygame.display.flip()
          clock.tick(40)
if __name__ == "__main__":
     main()
    
