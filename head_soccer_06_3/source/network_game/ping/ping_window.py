__author__ = 'newtonis'

__author__ = 'ariel'

from source.data import fonts
from source.gui.window import Window
from source.gui.text import Text
from utils import *

class PingWindow(Window):
    def __init__(self):
        Window.__init__(self,"High ping",(36, 107, 97),(43, 76, 111),0,0,400,150,(255,255,255))
        textTitle = Text(fonts.BebasNeue.c30,"Your ping is too high",(255,255,255),0,0)
        textTitle.x = self.width / 2 - textTitle.surface.get_size()[0]/2
        textTitle.y = 60
        self.AddElement(textTitle,"info")

        currentPing = Text(fonts.BebasNeue.c40,"",(255,255,255))
        currentPing.x = self.width / 2 - textTitle.surface.get_size()[0]/2
        currentPing.y = 90
        self.AddElement(currentPing,"ping")
    def SetPing(self,ping):
        self.references["ping"].text  = gPingText(ping)
        self.references["ping"].color = gPingColor(ping)
        self.references["ping"].x = self.width/2-self.references["ping"].surface.get_size()[0]/2
        self.references["ping"].Render()
    def ExtraLogicUpdate(self):
        self.parent.AddUpdateRect(self.x,self.y,self.width,self.height+30)
