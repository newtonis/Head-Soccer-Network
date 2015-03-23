__author__ = 'newtonis'

from pygame.surface import *
from source.gui.element import Element
from source.gui.bar import Bar

class Console(Element):
    def __init__(self,size,position):
        self.x,self.y = size
        self.width , self.height = size
        self.background = (0,0,0)
        self.textColor = (255,255,255)
        self.bar = Bar(5,self.height,1,self.width,0,(100,100,100),(200,200,200))
        self.texts = []
    def LogicUpdate(self):
        pass
    def AddMessage(self,msj):
        self.texts.append(msj)
    def GraphicUpdate(self,screen):
        my_surface = Surface((self.width,self.height))
        my_surface.fill(self.background)
