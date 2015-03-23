__author__ = 'newtonis'
import pygame
class RectManager:
    def __init__(self):
        self.rects = []
    def AddUpdateRect(self,x,y,w,h):
        self.rects.append([x,y,w,h])
    def ScreenBlit(self):
        pygame.display.update(self.rects)
        self.rects = []