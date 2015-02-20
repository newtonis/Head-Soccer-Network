__author__ = 'newtonis'

from window import Window
from text import Text
from source.data import fonts
from button import *


#### This file contains the window that is opened before you exit a playing game (warning window)###
class CheckExit(Window):
    def __init__(self):
        Window.__init__(self,"Exit",(36, 107, 97),(52, 52, 119),0,0,400,100,(255,255,255),200)
        text = Text(fonts.BebasNeue.c20,"do you want to quit?",(255,255,255))
        text.x = self.width/2-text.surface.get_size()[0]/2
        text.y = 30
        self.AddElement(text,"Text")

        buttonExit = AcceptButton("Yes",100)
        buttonExit.y = 60
        buttonExit.x = self.width/4*3 - buttonExit.imageA.get_size()[0]/2
        self.AddElement(buttonExit,"Exit")

        buttonContinue = RejectButton("No",100)
        buttonContinue.y = 60
        buttonContinue.x = self.width/4 - buttonContinue.imageA.get_size()[0]/2
        self.AddElement(buttonContinue,"NoQuit")
    def ExtraLogicUpdate(self):
        if self.ButtonCheck("Exit"):
            self.parent.noCheckExit = False
            self.parent.ReturnRoomList()
        if self.ButtonCheck("NoQuit"):
            self.parent.noCheckExit = False
            self.parent.Kill(self)
