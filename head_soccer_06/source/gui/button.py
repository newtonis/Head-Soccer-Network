__author__ = 'ariel'
import pygame

from source.data import images, fonts
from source.gui.element import *
from source.gui.addBorder import *
from source.gui.getCenter import *
from source.gui.RoundedCorners import *
from source.gui.mouseIcon import *
import pygame.gfxdraw
import source.data.mouse as mouse

class BUTTON_IMAGES:
    class CLASSIC:
        NORMAL , \
        FOCUSED , \
        PRESSED = range(3)
    class CONNECT:
        NORMAL, \
        FOCUSED, \
        PRESSED = range(3,6)
def ButtonImage(text,background,type,size=None):
    ###### BUTTON DRAW ######


    ###### CLASSIC BUTTON #####
    if type == BUTTON_IMAGES.CLASSIC.NORMAL:
        textFont = fonts.PixelSplitter.c11.render(text,0,(0,0,0))
        if size == None:
            tfw,tfh = textFont.get_size()
        else:
            tfw,tfh = size
        surface  = pygame.surface.Surface((tfw+20,16))
        surface.fill(background)
        AddBorder(surface,1, (0,0,0))
        surface.blit(textFont,GetCenter(surface,textFont))
        return surface
    elif type == BUTTON_IMAGES.CLASSIC.FOCUSED:
        textFont = fonts.PixelSplitter.c12.render(text,0,(0,0,0))
        if size == None:
            tfw,tfh = textFont.get_size()
        else:
            tfw,tfh = size
        surface = pygame.surface.Surface((tfw+20,16))
        surface.fill(background)
        AddBorder(surface,2,(0,0,0))
        surface.blit(textFont,GetCenter(surface,textFont))
        return surface
    elif type == BUTTON_IMAGES.CLASSIC.PRESSED:
        textFont = fonts.PixelSplitter.c13.render(text,0,(0,0,0))
        if size == None:
            tfw,tfh = textFont.get_size()
        else:
            tfw,tfh = size
        surface = pygame.surface.Surface((tfw+20,16))
        surface.fill(background)
        AddBorder(surface,3,(0,0,0))
        surface.blit(textFont,GetCenter(surface,textFont))
        return surface



    ###### CONNECT BUTTON #####
    elif type == BUTTON_IMAGES.CONNECT.NORMAL:
        textFont = fonts.BebasNeue.c60.render(text,1,(0,0,0))
        tfw, tfh = textFont.get_size()
        surface = pygame.surface.Surface((tfw+300,80))
        images.FillWithColor(surface,(255,255,0),(200,200,0))
        AddBorder(surface,1,(0,0,0))
        surface.blit(textFont,GetCenter(surface,textFont))
        return surface
    elif type == BUTTON_IMAGES.CONNECT.FOCUSED:
        textFont = fonts.BebasNeue.c60.render(text,1,(100,100,100))
        tfw, tfh = textFont.get_size()
        surface = pygame.surface.Surface((tfw+300,80))
        images.FillWithColor(surface,(255,255,0),(200,200,0))
        AddBorder(surface,4,(0,0,0))
        surface.blit(textFont,GetCenter(surface,textFont))
        return surface
    elif type == BUTTON_IMAGES.CONNECT.PRESSED:
        textFont = fonts.BebasNeue.c60.render(text,1,(0,0,0))
        tfw, tfh = textFont.get_size()
        surface = pygame.surface.Surface((tfw+300,80))
        images.FillWithColor(surface,(100,100,0),(200,200,0))
        AddBorder(surface,4,(0,0,0))
        surface.blit(textFont,GetCenter(surface,textFont))
        return surface
class Button(Element):
    def __init__(self,imageA,imageB,imageC,position):
        Element.__init__(self,position)
        self.imageA = imageA
        self.imageB = imageB
        self.imageC = imageC
        self.size = self.imageA.get_size()
        self.focused = False
        self.pressed = False
    def LogicUpdate(self):
        if not self.enabled:
            self.focused = False
            self.pressed = False
            return

        mousePos = self.GetMouse()
        pressed = self.GetPressed()
        ff = False
        pp = False
        if mousePos[0] > self.x and mousePos[0] < self.x + self.size[0]:
            if mousePos[1] > self.y and mousePos[1] < self.y + self.size[1]:
                ff = True
                if pressed:
                    pp = True
        self.focused = ff
        self.pressed = pp
    def GraphicUpdate(self,screen):
        if not self.focused:
            screen.blit(self.imageA,(self.x,self.y))
        elif not self.pressed:
            screen.blit(self.imageB,(self.x,self.y))
            SetHand()
        else:
            screen.blit(self.imageC,(self.x,self.y))

class TriImageButton(Button):
    def __init__(self,text,background,button_class_image,position):
        imageA = ButtonImage(text,background,button_class_image.NORMAL)
        imageB = ButtonImage(text,background,button_class_image.FOCUSED)
        imageC = ButtonImage(text,background,button_class_image.PRESSED)
        Button.__init__(self,imageA,imageB,imageC,position)

class ClassicButton(TriImageButton):
    def __init__(self,text,background,position):
        self.text       = text
        self.background = background

        TriImageButton.__init__(self,text,background,BUTTON_IMAGES.CLASSIC,position)

class ConnectButton(TriImageButton):
    def __init__(self,text,position):
        self.text = text
        TriImageButton.__init__(self,text,(0,0,0),BUTTON_IMAGES.CONNECT,position)

class AcceptButton(Button):
    def __init__(self,text,width=200,position=(0,0),font=fonts.BebasNeue.c30):
        self.text = text
        text = fonts.BebasNeue.c30.render(text,1,(255,255,255))

        imageA = pygame.surface.Surface((width,text.get_size()[1]+5))
        images.FillWithColor(imageA,(0,0,0),(00,100,0))
        imageA.blit(text,GetCenter(imageA,text))
        AddBorder(imageA)

        imageB = pygame.surface.Surface((width,text.get_size()[1]+5))
        images.FillWithColor(imageB,(0,50,0),(0,150,0))
        imageB.blit(text,GetCenter(imageB,text))
        AddBorder(imageB)

        imageC = pygame.surface.Surface((width,text.get_size()[1]+5))
        images.FillWithColor(imageC,(0,100,0),(0,200,0))
        imageC.blit(text,GetCenter(imageC,text))
        AddBorder(imageC)

        Button.__init__(self,imageA,imageB,imageC,position)

class RejectButton(Button):
    def __init__(self,text,width=200,position=(0,0),font=fonts.BebasNeue.c30):
        self.text = text
        text = fonts.BebasNeue.c30.render(text,1,(255,255,255))

        imageA = pygame.surface.Surface((width,text.get_size()[1]+5))
        images.FillWithColor(imageA,(0,0,0),(100,0,0))
        imageA.blit(text,GetCenter(imageA,text))
        AddBorder(imageA)

        imageB = pygame.surface.Surface((width,text.get_size()[1]+5))
        images.FillWithColor(imageB,(50,0,0),(150,0,0))
        imageB.blit(text,GetCenter(imageB,text))
        AddBorder(imageB)

        imageC = pygame.surface.Surface((width,text.get_size()[1]+5))
        images.FillWithColor(imageC,(100,0,0),(200,0,0))
        imageC.blit(text,GetCenter(imageC,text))
        AddBorder(imageC)

        Button.__init__(self,imageA,imageB,imageC,position)

class NeutralButton(Button):
    def __init__(self,text,width=200,position=(0,0),font=fonts.BebasNeue.c30):
        self.text = text
        text = font.render(text,1,(255,255,255))

        imageA = pygame.surface.Surface((width,text.get_size()[1]+5))
        images.FillWithColor(imageA,(0,0,0),(0,0,100))
        imageA.blit(text,GetCenter(imageA,text))
        AddBorder(imageA)

        imageB = pygame.surface.Surface((width,text.get_size()[1]+5))
        images.FillWithColor(imageB,(0,0,50),(0,0,150))
        imageB.blit(text,GetCenter(imageB,text))
        AddBorder(imageB)

        imageC = pygame.surface.Surface((width,text.get_size()[1]+5))
        images.FillWithColor(imageC,(0,0,100),(0,0,200))
        imageC.blit(text,GetCenter(imageC,text))
        AddBorder(imageC)

        Button.__init__(self,imageA,imageB,imageC,position)

def EfectoGota(size,initial_color,end_color,start_from,difference):
    surface = pygame.Surface(size)
    if difference[0] > 0:
        max_distance = size[0]/2+difference[0]
    else:
        max_distance = size[0]/2-difference[0]
    max_size = max_distance+50
    div = max_size/20
    extras = []
    position = (size[0]/2+difference[0],size[1]/2+difference[1])
    for x in range(div-1,0,-1):
        end = 0
        for y in range(max_size/div,end,-1):
            color = images.GetInter(initial_color,end_color,max_size/div-y,max_size/div)
            radius = (max_size/div)*x+y+start_from
            if radius > max_size:
                radius = radius-max_size+max_size/10
                extras.append([radius,color])
            else:
                pygame.gfxdraw.filled_circle(surface,position[0],position[1],radius,color)
        for x in range(len(extras)):
            pygame.gfxdraw.filled_circle(surface,position[0],position[1],extras[x][0],extras[x][1])
        ant_initial = initial_color
        initial_color = end_color
        end_color = ant_initial
    return surface

class AdvancedButton(Element):
    def __init__(self,size,position,text,starting_color,end_color):
        Element.__init__(self,position)
        self.w,self.h = size
        self.state = BUTTON_IMAGES.CONNECT.NORMAL
        self.x,self.y = position
        self.image = None
        self.text = text
        self.text_render = None
        self.start_from = 0
        self.difference = [0,0]
        self.starting_color = starting_color
        self.end_color = end_color
        self.temporal_x = self.x
        self.temporal_y = self.y
        self.GenerateButton()
        self.moving = True
        self.pressed = False
    def GenerateModifiedColor(self,color,difference):
        new_color = [color[0]+difference,color[1]+difference,color[2]+difference]
        if new_color[0] > 255:
            new_color[0] = 255
        if new_color[1] > 255:
            new_color[1] = 255
        if new_color[2] > 255:
            new_color[2] = 255
        return new_color
    def GenerateButton(self):
        self.image = EfectoGota((self.w,self.h),self.starting_color,self.end_color,self.start_from,self.difference)
        AddBorder(self.image,2,(255,0,0))
    def GraphicUpdate(self,screen):
        if self.state == BUTTON_IMAGES.CONNECT.NORMAL:
            self.temporal_x = self.x
            self.temporal_y = self.y
        color_font = (255,0,0)
        if self.state == BUTTON_IMAGES.CONNECT.NORMAL:
            self.text_render = fonts.BebasNeue.c50.render(self.text,1,color_font)
        else:
            self.text_render = fonts.BebasNeue.c60.render(self.text,1,color_font)
        screen.blit(self.image,(self.temporal_x,self.temporal_y))
        self.pos_text = [self.x+self.w/2-self.text_render.get_size()[0]/2,self.y+self.h/2-self.text_render.get_size()[1]/2]
        screen.blit(self.text_render,self.pos_text)
    def LogicUpdate(self):
        self.pressed = False
        if self.moving:
            self.image = EfectoGota((self.w,self.h),self.starting_color,self.end_color,self.start_from,self.difference)
            if self.state == BUTTON_IMAGES.CONNECT.NORMAL:
                AddBorder(self.image,2,(0,100,255))
            else:
                AddBorder(self.image,3,(0,100,255))
            self.start_from += 2
        if self.start_from >= self.w/2 or self.start_from <= 0:
            self.start_from = 0
        x_pos,y_pos = self.GetMouse()
        self.state = BUTTON_IMAGES.CONNECT.NORMAL
        if x_pos > self.x and x_pos < self.x + self.w:
            if y_pos > self.y and y_pos < self.y + self.h:

                if self.GetPressed():
                    self.state = BUTTON_IMAGES.CONNECT.PRESSED
                    self.pressed = True
                else:
                    self.state = BUTTON_IMAGES.CONNECT.FOCUSED
                    self.moving = True
                    SetHand()
                    if self.state != BUTTON_IMAGES.CONNECT.PRESSED:
                        self.difference = [x_pos - (self.x + self.w/2), y_pos - (self.y + self.h/2)]
