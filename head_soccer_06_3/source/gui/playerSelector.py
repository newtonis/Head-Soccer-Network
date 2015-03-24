__author__ = 'newtonis'
import pygame
from source.data import fonts
from source.data.images import Heads
from source.gui.button import *
from source.gui.element import Element
from source.gui.text import Text
from source.gui.surface import Surface

class PlayerSelector(Element):
    def __init__(self,players,width,height,parent,position):
        self.parent = parent
        Element.__init__(self,position)
        self.width = width
        self.height = height

        self.players = players
        self.CurrentPlayer = 0

        self.buttonPrevious = NeutralButton("Previous",font=fonts.BebasNeue.c20,width=100)
        self.buttonPrevious.x = 10
        self.buttonPrevious.y = height/2 - self.buttonPrevious.imageA.get_size()[1]/2
        self.buttonPrevious.parent = self
        self.buttonPrevious.fix = True
        self.buttonPrevious.enabled = True

        self.buttonNext = NeutralButton("Next",font=fonts.BebasNeue.c20,width=100)
        self.buttonNext.x = width-self.buttonNext.imageA.get_size()[0]-10
        self.buttonNext.y = height/2- self.buttonNext.imageA.get_size()[1]/2
        self.buttonNext.parent = self
        self.buttonNext.fix = True
        self.buttonNext.enabled = True


        #### HEAD TEXT AND HEAD IMAGE ####
        self.headCodeText = None
        self.headImage = Surface()

        self.previousPressed = False
        self.nextPressed = False
        self.UpdateHead()
    def SetCurrent(self,current):
        for head_x in range(len(self.players)):
            if self.players[head_x] == current:
                self.CurrentPlayer = head_x
                break
        self.UpdateHead()
    def UpdateHead(self):
        self.SetHead(self.players[self.CurrentPlayer])
    def SetHead(self,headCode):
        headCodeText = Text(fonts.BebasNeue.c25,headCode,(255,255,255))
        headCodeText.y = self.y-10
        headCodeText.x = self.width/2 - headCodeText.surface.get_size()[0]/2
        self.headCodeText = headCodeText

        self.headImage.ChangeImage(Heads.codes[headCode][0])
        self.headImage.y = self.height/2-self.headImage.GetSize()[1]/2
        self.headImage.x = self.width/2-self.headImage.GetSize()[0]/2

    def GraphicUpdate(self,screen):
        my_surface = pygame.surface.Surface((self.width,self.height),pygame.SRCALPHA)

        self.buttonPrevious.GraphicUpdate(my_surface)
        self.buttonNext.GraphicUpdate(my_surface)
        if self.headCodeText:
            print self.headCodeText.x,self.headCodeText.y
            self.headCodeText.GraphicUpdate(screen)
        if self.headImage:
            self.headImage.GraphicUpdate(my_surface)
        if self.buttonNext.pressed and not self.nextPressed:
            self.nextPressed = True
            self.GoNext()
        if not self.buttonNext.pressed:  ## MAQ-ESTADOS ##
            self.nextPressed = False
        if self.buttonPrevious.pressed and not self.previousPressed:
            self.previousPressed = True
            self.GoBack()
        if not self.buttonPrevious.pressed: ## MAQ-ESTADOS ##
            self.previousPressed = False
        screen.blit(my_surface,(self.x,self.y))
    def LogicUpdate(self):
        self.buttonPrevious.LogicUpdate()
        self.buttonNext.LogicUpdate()
    def GoNext(self):
        if self.CurrentPlayer < len(self.players)-1:
            self.CurrentPlayer += 1
        else:
            self.CurrentPlayer = 0
        self.UpdateHead()
    def GoBack(self):
        if self.CurrentPlayer > 0:
            self.CurrentPlayer -= 1
        else:
            self.CurrentPlayer = len(self.players)-1
        self.UpdateHead()
    def GetHeadCode(self):
        return self.players[self.CurrentPlayer]
