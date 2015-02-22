from source.data import images, fonts

__author__ = 'ariel'

import pygame

from source.gui.element import Element
from source.gui.getCenter import GetCenter
from source.gui.bar import Bar
from source.data import images,fonts


class Key:
    def __init__(self,title,length,background):
        self.title = title
        self.length = length
        self.background = background
        self.GenerateSurface()
    def GenerateSurface(self):
        text = fonts.BebasNeue.c30.render(self.title,1,(255,255,255))
        surface = pygame.surface.Surface((self.length,50))
        #images.FillWithBack(surface, images.Backgrounds.back1)
        images.FillWithColor(surface,self.background[0],self.background[1])
        surface.blit(text,GetCenter(surface,text))
        self.surface = surface

class ContentRow:
    def __init__(self,keysContent,keys,color):
        self.content = keysContent
        self.keys = keys
        self.selected = False
        self.backA, self.backB = color
        self.GenerateSurface()
    def GenerateSurface(self):
        #text = fonts.BebasNeue.c25.render(self)
        surfaces = []

        x_sum = 0
        for key in self.keys:
            key_name = key.title
            key_length = key.length
            surfaceA = pygame.surface.Surface((key_length,30),pygame.SRCALPHA)
            surfaceB = pygame.surface.Surface((key_length,30),pygame.SRCALPHA)

            background = pygame.surface.Surface((key_length,30))
            #images.FillWithBack(background, images.Backgrounds.back6)
            images.FillWithColor(background,self.backA,self.backB)

            surfaceB.blit(background,(0,0))
            background.set_alpha(50)
            surfaceA.blit(background,(0,0))

            text = fonts.BebasNeue.c25.render(self.content[key_name],1,(255,255,255))
            surfaceA.blit(text,GetCenter(surfaceA,text))
            surfaceB.blit(text,GetCenter(surfaceB,text))

            x_sum += key_length + 1
            surfaces.append({"ss":surfaceA,"s2":surfaceB,"ww":key_length})

        finalSurface = pygame.surface.Surface((x_sum,30),pygame.SRCALPHA)
        finalSurfaceB = pygame.surface.Surface((x_sum,30),pygame.SRCALPHA)
        actual_x = 0
        for s in surfaces:
            finalSurface.blit(s["ss"],(actual_x,0))
            finalSurfaceB.blit(s["s2"],(actual_x,0))
            actual_x += s["ww"]+1
        self.surface = finalSurface
        self.surfaceB= finalSurfaceB
    def GetSurface(self):
        if self.selected:
            return self.surfaceB
        else:
            return self.surface
    def Select(self):
        self.selected = True
    def UnSelect(self):
        self.selected = False

class ListSystem(Element):
    def __init__(self,x,y,selectable=False,height=300):
        Element.__init__(self,(x,y))
        self.keys = []
        self.contents = []
        self.margin_y = 0
        self.selectable = True
        self.x = x
        self.y = y
        self.width = 0
        self.selected = -1
        self.enabled = False
        self.height = height
        self.bar = None
        self.SetBackground((20,0,0),(50,0,0))
        self.SetItemColor((41,0,69),(149,0,255))
        self.SetUpBackground((23,0,45),(86,0,173))
        self.sendInfoDef = None

        self.upPressed = False
        self.downPressed = False
    def SetSendInfoDef(self,func):
        self.sendInfoDef = func
    def SetBackground(self,backgroundA,backgroundB):
        self.background = backgroundA,backgroundB
    def SetItemColor(self,colorA,colorB):
        self.itemColor = colorA,colorB
    def SetUpBackground(self,backgroundA,backgroundB):
        self.upBack = backgroundA,backgroundB
    def AddRow(self,content):
        self.contents.append(ContentRow(content,self.keys,self.itemColor))
        if len(self.contents) > self.height / 30:
            if not self.bar:
                self.EnableBar()
            else:
                self.UpdateBar()
        else:
            if self.bar:
                self.DisableBar()
    def UpdateBar(self):
        self.bar.bar_size = self.GetBarSize()
    def EnableBar(self):
        self.bar = Bar(10,self.height,self.GetBarSize(),self.x+self.width-10,self.y+50,(100,100,100),(255,255,255))

        self.bar.parent = self.parent
        self.bar.enabled = True
    def DisableBar(self):
        self.bar = None
    def GetBarSize(self):
        my_height = self.height
        height_need = 30 * len(self.contents)
        return float(my_height) / float(height_need)
    def AddUpKey(self,title,length):
        self.keys.append(Key(title,length,self.upBack))
        self.width += length + 1
    def GraphicUpdate(self,screen):
        my_surface = pygame.surface.Surface((self.width,self.height+50))
        images.FillWithColor(my_surface,self.background[0],self.background[1])

        if self.bar:
            min_fix = 0
            max_fix = len(self.contents)*30-self.height
            fix = abs(min_fix-max_fix)*self.bar.position
            actual_y = 50 - fix
        else:
            actual_y = 50
        for row in self.contents:
            my_surface.blit(row.GetSurface(),(0,actual_y))
            actual_y += 30

        current_x = 0
        for key in self.keys:
            my_surface.blit(key.surface,(current_x,0))
            current_x += key.surface.get_size()[0] + 1

        screen.blit(my_surface,(self.x,self.y))
        if self.bar:
            self.bar.GraphicUpdate(screen)

    def LogicUpdate(self):
        if self.enabled:
            if self.bar:
                self.bar.LogicUpdate()
                if self.bar.pressed:
                    return
            mouse_x,mouse_y = self.GetMouse()
            mouse_x -= self.x
            mouse_y -= self.y

            if self.bar:
                min_fix = 0
                max_fix = len(self.contents)*30-self.height
                fix = abs(min_fix-max_fix)*self.bar.position
            else:
                fix = 0

            pressed = pygame.mouse.get_pressed()
            if pressed[0]:
                if mouse_x > 0 and mouse_x < self.width:
                    if mouse_y > 50 and mouse_y < self.height+50:
                        mouse_y -= 50
                        self.SetSelected(float(mouse_y+fix)/30.0)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and not self.upPressed:
                self.goUp()
                self.upPressed = True
            if not keys[pygame.K_UP]:
                self.upPressed = False
            if keys[pygame.K_DOWN] and not self.downPressed:
                self.goDown()
                self.downPressed = True
            if not keys[pygame.K_DOWN]:
                self.downPressed = False
    def goUp(self):
        nselected = self.selected - 1
        if nselected < 0:
            nselected = len(self.contents)
        self.SetSelected(nselected)
    def goDown(self):
        nselected = self.selected + 1
        if nselected >= len(self.contents):
            nselected = 0
        self.SetSelected(nselected)
    def SetSelected(self,selected):
        selected = int(selected)
        if self.sendInfoDef:
            self.sendInfoDef(selected)
        if selected >= len(self.contents):
            return
        self.contents[self.selected].UnSelect()
        self.selected = selected
        if self.selected != -1:
            self.contents[self.selected].Select()
    def ServerOpen(self):
        return self.contents[self.selected].content
    def DeleteRow(self,key,value):
        print "Deleting Row",key,":",value
        for cx in range(len(self.contents)):
            if self.contents[cx].content[key] == value:
                del self.contents[cx]
                return
    def UpdateRowValue(self,key,value,keyChange,newValue):
        print "Updating Row Value of",key,":",value
        for cx in range(len(self.contents)):
            if self.contents[cx].content[key] == value:
                self.contents[cx].content[keyChange] = newValue
                self.contents[cx].GenerateSurface()
