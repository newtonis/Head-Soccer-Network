__author__ = 'newtonis'

import pygame
import time

from source.gui.window import Window
from source.gui.text import Text
from source.gui.surface import Surface
from source.gui.button import *

from source.data import fonts

def ra06(number):
    if number < 10:
        return "0"+str(number)
    return str(number)
class MatchFinalWindow(Window):
    def __init__(self,data):
        Window.__init__(self,"Match statistics",(36, 107, 97),(36, 107, 97),0,0,500,300,(255,255,255),200)
        textWin = Text(fonts.CTProLamina.c40,data["textWin"],(255,255,255),0,0)
        textWin.y = 40
        textWin.x = self.width/2 - textWin.surface.get_size()[0]/2
        self.AddElement(textWin,"textWin")

        self.sum_y = 100

        self.SetGoalsFHalf(data["goalsData"])
        self.SetGoalsSHalf(data["goalsData"])
        self.SetGoalsFinal(data["goalsData"])

        self.ref = time.time()
        self.left = 20
        self.wait = 20

        self.AddTimeSurface()
    def SetGoalsFHalf(self,cdata):
        if not cdata.has_key("FH"):
            return
        data = cdata["FH"]
        textFHalf = Text(fonts.BebasNeue.c30,"1st",(255,255,255),0,0)
        textFHalf.y = self.sum_y - textFHalf.surface.get_size()[1]/2
        textFHalf.x = self.width/2 - textFHalf.surface.get_size()[0]/2
        self.AddElement(textFHalf,"textFHalf")

        textA = Text(fonts.BebasNeue.c40,str(data["A"]),(255,255,255))
        textA.y = self.sum_y - textA.surface.get_size()[1]/2
        textA.x = self.width/4 - textA.surface.get_size()[0]/2
        self.AddElement(textA,"first_half_A")

        textB = Text(fonts.BebasNeue.c40,str(data["B"]),(255,255,255))
        textB.y = self.sum_y - textB.surface.get_size()[1]/2
        textB.x = self.width/4*3 - textB.surface.get_size()[0]/2
        self.AddElement(textB,"first_half_B")

        self.sum_y += 40
    def SetGoalsSHalf(self,cdata):
        if not cdata.has_key("SH"):
            return
        data = cdata["SH"]
        textSHalf = Text(fonts.BebasNeue.c30,"2nd",(255,255,255),0,0)
        textSHalf.y = self.sum_y - textSHalf.surface.get_size()[1]/2
        textSHalf.x = self.width/2 - textSHalf.surface.get_size()[0]/2
        self.AddElement(textSHalf,"textSHalf")

        textA = Text(fonts.BebasNeue.c40,str(data["A"]),(255,255,255))
        textA.y = self.sum_y - textA.surface.get_size()[1]/2
        textA.x = self.width/4 - textA.surface.get_size()[0]/2
        self.AddElement(textA,"second_half_A")

        textB = Text(fonts.BebasNeue.c40,str(data["B"]),(255,255,255))
        textB.y = self.sum_y - textB.surface.get_size()[1]/2
        textB.x = self.width/4*3 - textB.surface.get_size()[0]/2
        self.AddElement(textB,"second_half_B")

        self.sum_y += 40
    def SetGoalsFinal(self,cdata):
        if not cdata.has_key("FN"):
            return

        self.sum_y += 0

        lineS = pygame.surface.Surface((300,1))
        lineS.fill((255,255,255))
        surfaceLine = Surface(lineS,(0,0))
        surfaceLine.x = self.width/2 - lineS.get_size()[0]/2
        surfaceLine.y = self.sum_y - lineS.get_size()[1]/2
        self.AddElement(surfaceLine,"line")

        self.sum_y += 40

        data = cdata["FN"]
        textFinal = Text(fonts.BebasNeue.c40,"final",(255,255,255),0,0)
        textFinal.y = self.sum_y - textFinal.surface.get_size()[1]/2
        textFinal.x = self.width/2 - textFinal.surface.get_size()[0]/2
        self.AddElement(textFinal,"textFinal")

        textA = Text(fonts.BebasNeue.c40,str(data["A"]),(255,255,255))
        textA.y = self.sum_y - textA.surface.get_size()[1]/2
        textA.x = self.width/4 - textA.surface.get_size()[0]/2
        self.AddElement(textA,"final_A")

        textB = Text(fonts.BebasNeue.c40,str(data["B"]),(255,255,255))
        textB.y = self.sum_y - textB.surface.get_size()[1]/2
        textB.x = self.width/4*3 - textB.surface.get_size()[0]/2
        self.AddElement(textB,"final_B")

        self.sum_y += 40
    def AddButtons(self):

        #playAgain = AcceptButton("Rematch")
        #playAgain.y = self.sum_y
        #playAgain.x = self.width/4 - playAgain.imageA.get_size()[0]/2
        #self.AddElement(playAgain,"PlayAgain")

        #Exit = RejectButton("Exit")
        #Exit.y = self.sum_y
        #Exit.x = self.width/4*3 - Exit.imageA.get_size()[0]/2
        #self.AddElement(Exit,"Exit")
        #self.sum_y += 40
        pass
    def AddTimeSurface(self):
        text = Text(fonts.BebasNeue.c40,str(self.wait)+" seconds left",(255,255,255))
        text.x = self.width/2 - text.surface.get_size()[0]/2
        text.y = self.sum_y
        self.AddElement(text,"MSJ")
    def UpdateTime(self,sec):
        self.references["MSJ"].text = ra06(sec)+" seconds left"
        self.references["MSJ"].Render()
    def ExtraLogicUpdate(self):
        if self.wait - int(time.time() - self.ref) != self.left:
            self.left = self.wait - int(time.time() - self.ref)
            self.UpdateTime(self.left)
        self.Refresh()
    def Refresh(self):
        self.AddUpdateRect(0,0,self.width,self.height+30)