__author__ = 'newtonis'

import time
from element import Element

class Surface(Element):
    def __init__(self,image=None,position=(0,0)):
        Element.__init__(self,position)
        self.image = image
    def ChangeImage(self,image=None):
        self.image = image
    def GraphicUpdate(self,screen):
        if self.image:
            screen.blit(self.image,(self.x,self.y))
    def LogicUpdate(self):
        pass
    def GetSize(self):
        if self.image:
            return self.image.get_size()
        else:
            return 0,0

class Animation(Surface):
    def __init__(self,animation,position,side = -1,frec=0.4):
        self.us = False
        self.side = side
        self.SetAnimation(animation)
        Surface.__init__(self,None,position)
        self.SetImageAnimation(0)

        self.frec = 5
        self.period = 1.0/self.frec
        self.playAnimation = False
        self.locked = False
    def SetParent(self,parent):
        self.parent = parent
    def SetUpdateSS(self):
        self.us = True
    def SetFrec(self,frec):
        self.frec = frec
        self.period = 1.0/self.frec
    def StartAnimation(self,stopEnd=True):
        if not self.playAnimation and not self.locked:
            self.ref = time.time()*1000
            self.playAnimation = True
            self.stopEnd = stopEnd
            self.locked = True
    def Unclock(self):
        self.locked = False
    def SetSide(self,side):
        self.side = side
    def SetAnimation(self,animation):
        self.animation = animation
    def SetImageAnimation(self,x):
        self.current = x
        if self.side != -1:
            self.image = self.animation[self.current][self.side]
        else:
            self.image = self.animation[self.current]

        if self.us:
            self.parent.AddUpdateRect(self.x,self.y,self.image.get_size()[0],self.image.get_size()[1])
    def Reset(self):
        self.SetImageAnimation(0)
        self.playAnimation = False
    def LogicUpdate(self):
        if self.playAnimation:
            length = len(self.animation)
            dt = time.time() * 1000 - self.ref
            current_image = int( float(length) * (float(dt)/(float(self.period*1000)) ) )

            if self.current != current_image:
                if current_image >= length:
                    if self.stopEnd:
                        self.SetImageAnimation(0)
                        self.playAnimation = False
                        self.locked = True
                    else:
                        self.ref = time.time() * 1000
                else:
                    self.SetImageAnimation(current_image)
