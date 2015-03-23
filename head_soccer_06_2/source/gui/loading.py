__author__ = 'newtonis'

import pygame
import time
from element import Element
from getCenter import GetCenter
from pygame.draw import *
from pygame.surface import *

class LoadingAnimation(Element):
    def __init__(self,frec=0.4,squares=5,color=(0,150,0),x=0,y=0):
        self.squares = squares
        self.frec = frec #hz
        self.period = 1.0/float(self.frec)
        self.x = x
        self.y = y
        self.color = color
        self.current_square = 0
        self.square_period = 0
        self.start_time = time.time()*1000
        self.width = self.squares*26
        self.height = 30
        self.max_big = 20
        self.min_big = 10
    def GraphicUpdate(self,screen):
        surface = Surface((self.squares*26,30),pygame.SRCALPHA)

        for s in range(self.squares):
            if s == self.current_square:
                if self.square_period > 4:
                    sq = 10 - self.square_period
                else:
                    sq = self.square_period
                size = sq / 5.0 * (self.max_big-self.min_big)
                square_surface = Surface((size+self.min_big,size+self.min_big))
                square_surface.fill(self.color)
                surface.blit(square_surface,(s*26-square_surface.get_size()[0]/2+13,GetCenter(surface,square_surface)[1]))
            else:
                square_surface = Surface((self.min_big,self.min_big))
                square_surface.fill(self.color)
                surface.blit(square_surface,(s*26-square_surface.get_size()[0]/2+13,GetCenter(surface,square_surface)[1]))
        screen.blit(surface,(self.x,self.y))

    def LogicUpdate(self):
        dt = ( time.time()*1000 - self.start_time ) % (self.period*1000)
        fraction = float(dt) / float(self.period*1000)
        current_square = int( fraction / (1.0/float(self.squares)) )
        rest_abs = ( fraction - current_square * (1.0/float(self.squares)) )
        rest_rel = int(rest_abs / (1.0/float(self.squares)) * 10.0)

        self.current_square = current_square
        self.square_period = rest_rel

def main():
    loading = LoadingAnimation()
    screen = pygame.display.set_mode((800,600))
    #loading.x = screen.get_size()[0]/2-loading.width
    #loading.y = screen.get_size()[1]/2-loading.height

    continuar = True
    while continuar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuar = False
        screen.fill((255,255,255))
        loading.LogicUpdate()
        loading.GraphicUpdate(screen)
        pygame.display.update()
if __name__ == "__main__":
    main()