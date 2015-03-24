__author__ = 'Dylan'

from source.gui.element import Element
from source.gui.addBorder import AddBorder
from source.data import images
import pygame

class CheckBox(Element):
    def __init__(self,parent,size,default_checked = False):
        Element.__init__(self,(0,0))
        self.parent = parent
        self.w,self.h = size
        self.default = default_checked
        self.img = images.Checkbox.checkbox
        self.img_checked = images.Checkbox.checkbox_checked
        self.checked = self.default
        self.GenerateSurfaces()
        self.last_pressed = False
    def GenerateSurfaces(self):
        self.img = pygame.transform.scale(self.img,(self.w,self.h))
        self.img_checked = pygame.transform.scale(self.img_checked,(self.w,self.h))
    def GraphicUpdate(self,screen):
        if self.checked:
            surf = self.img_checked
        else:
            surf = self.img
        screen.blit(surf,(self.x,self.y))
    def LogicUpdate(self):
        x,y = self.GetMouse()
        if self.GetPressed():
            if not self.last_pressed:
                self.last_pressed = True
                if x > self.x and y > self.y and x < self.x + self.w and y < self.y + self.h:
                    if self.checked:
                        self.checked = False
                    else:
                        self.checked = True
        else:
            self.last_pressed = False