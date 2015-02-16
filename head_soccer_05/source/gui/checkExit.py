__author__ = 'newtonis'

from window import Window
from text import Text
from source.data import fonts
from button import *

class CheckExit(Window):
    def __init__(self):
        Window.__init__(self,"Exit",(255,0,0),(36, 107, 97),0,0,600,140,(255,255,255),255)
        text = Text(fonts.BebasNeue.c20,"Are you sure you want to quit?",(255,255,255))
        text.x = self.width/2-text.surface.get_size()[0]/2
        text.y = 40
        self.AddElement(text,"Text")

        buttonExit = AcceptButton("Yes")
        buttonExit.y = 90
        buttonExit.x = self.width/4*3 - buttonExit.imageA.get_size()[0]/2
        self.AddElement(buttonExit,"Exit")

        buttonContinue = RejectButton("No")
        buttonContinue.y = 90
        buttonContinue.x = self.width/4 - buttonContinue.imageA.get_size()[0]/2
        self.AddElement(buttonContinue,"NoQuit")
    def ExtraLogicUpdate(self):
        if self.ButtonCheck("Exit"):
            self.parent.noCheckExit = False
            self.parent.ReturnRoomList()
        if self.ButtonCheck("NoQuit"):
            self.parent.noCheckExit = False
            self.parent.Kill(self)
