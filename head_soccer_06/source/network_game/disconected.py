__author__ = 'newtonis'

from source.data import fonts
from source.gui.window import Window
from source.gui.button import NeutralButton
from source.gui.text import Text

class DisconectedWindow(Window):
    def __init__(self):
        Window.__init__(self,"Connection lost",(200,100,100),(43, 76, 111),0,0,400,120,(0,0,0),255)

        textContent = Text(fonts.BebasNeue.c30,"Network game server conection lost",(255,255,255))
        textContent.y = 50
        textContent.x = self.width/2-textContent.surface.get_size()[0]/2
        self.AddElement(textContent)

        ButtonAccept = NeutralButton("OK")
        ButtonAccept.y = 90
        ButtonAccept.x = self.width/2-ButtonAccept.imageA.get_size()[0]/2
        self.AddElement(ButtonAccept,"Accept")
    def ExtraLogicUpdate(self):
        if not self.enabled:
            return
        if self.references["Accept"].pressed:
            self.parent.locked = False
            self.Kill()
