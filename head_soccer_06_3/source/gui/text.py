__author__ = 'ariel'
from source.gui.element import Element
from source.data import fonts


class Text(Element):
    def __init__(self,font,text,color,x=0,y=0,antialias=1):
        self.text = text
        self.font = font
        self.color = color
        self.antialias = antialias
        self.x = x
        self.y = y
        self.Render()
    def Render(self):
        self.surface = self.font.render(self.text,self.antialias,self.color)
    def LogicUpdate(self):
        pass
    def GraphicUpdate(self,screen):
        screen.blit(self.surface,(self.x,self.y))

class Title(Text):
    def __init__(self,text,color,x,y):
        Text.__init__(self, fonts.BebasNeue.c40,text,color,x,y)
