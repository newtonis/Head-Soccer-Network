__author__ = 'newtonis'

import threading
from source.data import *
from source.gui.text import Text
from source.gui.input import Input
from source.gui.window import Window
from source.gui.button import *
from source.database import serverQ

class ConfigWindow(Window):
    def __init__(self):
        Window.__init__(self,"Client sync configuration",(43, 76, 111),(117, 108, 163),0,0,400,170,(255,255,255),255)

        self.AddInput()
        self.AddAcceptButtons()

    def AddInput(self):
        interpolationConstantText = Text(fonts.BebasNeue.c20,"Interpolation constant:",(255,255,255))
        interpolationConstantText.y = 60 - interpolationConstantText.surface.get_size()[1]/2
        interpolationConstantText.x = self.width/4 - interpolationConstantText.surface.get_size()[0]/2
        self.AddElement(interpolationConstantText,"textIC")

        interpolationConstantInput = Input()
        interpolationConstantInput.AllowNumbers()
        interpolationConstantInput.SetSize(100,30)
        interpolationConstantInput.y = 60 - interpolationConstantInput.size[1]/2
        interpolationConstantInput.x = self.width/4*3 - interpolationConstantInput.size[0]/2
        interpolationConstantInput.text = str(config.interpolation_constant)
        self.AddElement(interpolationConstantInput,"IConstant")

        thresholdText = Text(fonts.BebasNeue.c20,"Threshold correction:",(255,255,255))
        thresholdText.y = 100 - thresholdText.surface.get_size()[1]/2
        thresholdText.x = self.width/4 - thresholdText.surface.get_size()[0]/2
        self.AddElement(thresholdText,"textTH")

        thresholdInput = Input()
        thresholdInput.AllowNumbers()
        thresholdInput.SetSize(100,30)
        thresholdInput.y = 100 - thresholdInput.size[1]/2
        thresholdInput.x = self.width/4*3 - thresholdInput.size[0]/2
        thresholdInput.text = str(config.threshold)
        self.AddElement(thresholdInput,"TH")
    def AddAcceptButtons(self):
        acceptButton = AcceptButton("ACCEPT",130)
        acceptButton.y = 130
        acceptButton.x = self.width/4 - acceptButton.imageA.get_size()[0]/2
        self.AddElement(acceptButton,"accept")

        cancelButton = RejectButton("CANCEL",130)
        cancelButton.y = 130
        cancelButton.x = self.width/4*3 - cancelButton.imageA.get_size()[0]/2
        self.AddElement(cancelButton,"cancel")
    def GetIC(self):
        return self.references["IConstant"].text
    def GetTH(self):
        return self.references["TH"].text
    def IsCorrect(self,value):
        try:
            nvalue = float(value)
        except:
            return False
        if nvalue > 0.0 and nvalue < 5.0:
            return True
    def ExtraLogicUpdate(self):
        if self.ButtonCheck("accept"):
            self.Send()
        if self.ButtonCheck("cancel"):
            self.Kill()
        self.parent.AddUpdateRect(self.x,self.y,self.width,self.height+30)
    def Send(self):
        self.Kill()
        if not self.IsCorrect(self.GetIC()) or not self.IsCorrect(self.GetTH()):
           self.Fail()
           return
        nIC = float(self.GetIC())
        nTH = float(self.GetTH())
        config.interpolation_constant = nIC
        config.threshold = nTH
        threadDB = threading.Thread(target=self.UpdateDB)
        threadDB.start()
    def UpdateDB(self):
        serverQ.UpdateConfig(config.threshold,config.interpolation_constant)

    def Fail(self):
        textFail = Text(fonts.BebasNeue.c17,"Are you crazy?!?! try again",(255,255,255))
        textFail.y = 25
        textFail.x = self.width/2 - textFail.surface.get_size()[0]/2
        self.AddElement(textFail,"fail")

        self.references["IConstant"].SetBackgroundColor(200,0,0)
        self.references["TH"].SetBackgroundColor(200,0,0)