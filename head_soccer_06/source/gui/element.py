__author__ = 'ariel'
import pygame

class Element:
    def __init__(self,position):
        self.x = position[0]
        self.y = position[1]
        self.enabled = False
        self.fix = False
    def SetParent(self,parent):
        self.parent = parent
    def LogicUpdate(self):
        pass
    def GraphicUpdate(self,screen):
        pass
    def GetMouse(self):
        pos = pygame.mouse.get_pos()
        if not self.fix:
            return pos[0] - self.parent.x , pos[1] - self.parent.y
        else:
            return pos[0] - self.parent.x - self.parent.parent.x , pos[1] - self.parent.y - self.parent.parent.y
    def GetPressed(self):
        pressed = pygame.mouse.get_pressed()
        return pressed[0]
    def Event(self,e):
        pass