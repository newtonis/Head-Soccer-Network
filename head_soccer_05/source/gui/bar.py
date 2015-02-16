__author__ = 'ariel'

import pygame

from addBorder import AddBorder
from source.gui.element import Element


class Bar(Element):
    def __init__(self,width,height,bar_size,x,y,bar_color=(0,0,255),bar_background=(255,255,255),border_color=(0,0,0)):
        self.enabled = False
        self.width = width
        self.height = height
        self.bar_size = bar_size
        self.x = x
        self.y = y
        self.position = 0
        self.focused = False
        self.pressed = False
        self.bar_color = bar_color
        self.bar_background = bar_background
        self.border_color = border_color
    def LogicUpdate(self):
        if not self.enabled:
            return
        pressed = pygame.mouse.get_pressed()
        mouse_x,mouse_y = self.GetMouse()
        if self.Focused(mouse_x,mouse_y):
            self.focused = True
            if pressed[0]:
                self.pressed = True
        if not pressed[0]:
            self.pressed = False
        if self.pressed:
            BarY = mouse_y - self.y - self.GetBarHeight()/2
            if self.height != self.GetBarHeight():
                self.SetBarPosition(float(BarY)/float(self.height- self.GetBarHeight()))
    def SetBarPosition(self,position):
        if position < 0:
            position = 0
        elif position > 1:
            position = 1
        self.position = position
    def Focused(self,mouse_x,mouse_y):
        if mouse_x >= self.x and mouse_x <= self.x + self.width:
            if mouse_y >= self.y and mouse_y < self.y + self.height:
                return True
        return False
    def GraphicUpdate(self,screen):
        my_surface = pygame.surface.Surface((self.width,self.height))
        my_surface.fill(self.bar_background)

        y_bar = self.GetBarY()
        surfaceBar = pygame.surface.Surface((self.width,self.GetBarHeight()))
        surfaceBar.fill(self.bar_color)
        my_surface.blit(surfaceBar,(0,y_bar))
        AddBorder(my_surface,1,self.border_color)
        screen.blit(my_surface,(self.x,self.y))
    def GetBarY(self):
        start_position = 0
        end_position = self.height - self.GetBarHeight()
        return (end_position-start_position)*self.position
    def GetBarHeight(self):
        return self.height * self.bar_size