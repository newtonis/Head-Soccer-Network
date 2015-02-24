__author__ = 'newtonis'

import pygame
from source.gui.getCenter import GetCenter

class WindowSystem:
    def __init__(self):
        self.windows = []
        self.references = dict()
        self.focused = -1
        self.eventable = -1
        self.locked = False
        self.screen = None
        self.events = None
    def SetScreen(self,screen):
        self.screen = screen
    def AddWindow(self,window,reference="NoReference"):
        self.windows.append(window)
        window.parent = self
        if reference != "NoReference":
            self.references[reference] = window
    def AddWindowCentered(self,window,screen=None,reference="NoReference"):
        if not screen:
            screen = self.screen
        window.x ,window.y = GetCenter(screen,window.surface)
        self.AddWindow(window,reference)
    def AddWindowCenteredOnFront(self,window,screen=None,reference="NoReference"):
        self.AddWindowCentered(window,screen,reference)
        if self.eventable != -1 and self.eventable < len(self.windows):
            self.windows[self.eventable].enabled = False
        self.eventable = len(self.windows)-1
        window.enabled = True
        window.locked = True
        self.locked = True
    def HandleWindows(self):
        for window in self.windows:
            window.LogicUpdate()
        if self.locked:
            return
        pressed = pygame.mouse.get_pressed()
        if pressed[0] and self.focused == -1:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            w_POS = self.GetFirstWindowIn(mouse_x,mouse_y)
            if w_POS == -1:
                return

            window = self.windows[w_POS]

            if self.eventable != -1:
                self.windows[self.eventable].enabled = False
            self.eventable = w_POS
            window.enabled = True


            del self.windows[w_POS]
            self.windows.append(window)

            if window.MouseClickIn(mouse_x,mouse_y):
                self.focused = w_POS
        if not pressed[0] and self.focused != -1:
            self.windows[self.focused].pressed = False
            self.focused = -1
    def GetFirstWindowIn(self,mouse_x,mouse_y):
        for x in range(len(self.windows)-1,-1,-1):
            if self.windows[x].MouseIsInto(mouse_x,mouse_y):
                return x
        return -1

    def Kill(self,window):
        self.locked = False
        for wk in range(len(self.windows)):
            if self.windows[wk] == window:
                del self.windows[wk]
                self.eventable = -1
                self.focused = -1
                return
    def DeleteWindow(self,reference):
        for wk in range(len(self.windows)):
            if self.references[reference] == self.windows[wk]:
                del self.windows[wk]
                del self.references[reference]
                return
    def DrawWindows(self,screen):
        for window in self.windows:
            window.GraphicUpdate(screen)
    def Event(self,e):
        self.events = e
        for window in self.windows:
            window.Event(e)
    def DeleteAllWindows(self):
        self.windows = []
        self.references = dict()