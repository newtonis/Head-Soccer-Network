__author__ = 'Dylan'

import pygame
from pygame.locals import *
from source.gui.addBorder import AddBorder
from source.gui.input import Input
from source.data.fonts import *
from source.data import fonts
from source.data.images import Extras
from source.gui.bar import Bar
from source.gui.pressAnalizer import PressAnalizer

import random

global font
font = CTProLamina

class MsgBox:
    def __init__(self,size,position,parent):
        global font
        self.parent = parent
        self.messages = []
        self.size = size
        self.background = pygame.transform.scale(Extras.void,self.size)
        self.x,self.y = position
        self.font_from = font.c22
        self.font_msg = font.c20
        self.writer_colors = []
    def GenerateSurface(self):
        surf = self.background.copy()
        y_pos = 0
        for y in range(len(self.messages)-1,-1,-1):
            msg = self.messages[y]
            if len(msg["Render"]["Msg"]) > 1:
                for x in range(len(msg["Render"]["Msg"])-1,0,-1):
                    global_y = self.size[1] - y_pos - msg["Render"]["From"].get_size()[1]
                    surf.blit(msg["Render"]["Msg"][x],(msg["Render"]["X From"],global_y))
                    y_pos += msg["Render"]["From"].get_size()[1]+2
            global_y = self.size[1] - y_pos - msg["Render"]["From"].get_size()[1]
            surf.blit(msg["Render"]["From"],(msg["Render"]["X From"],global_y))
            surf.blit(msg["Render"]["Msg"][0],(msg["Render"]["X Msg"],global_y))
            y_pos += msg["Render"]["From"].get_size()[1]+2
        return surf
    def GenerateRender(self,writer,msg):
        ret = {"From":None,"Msg":None,"Pos From":None,"Pos Msg":None}
        writer_exists = False
        writer_color = (random.randrange(0,150),random.randrange(0,150),random.randrange(0,150))
        for x in self.writer_colors:
            if x["Name"] == writer:
                writer_color = x["Color"]
                writer_exists = True
                break
            if x["Color"] == writer_color:
                writer_color = (random.randrange(150,255),random.randrange(150,255),random.randrange(150,255))
        if not writer_exists:
            self.writer_colors.append({"Name":writer,"Color":writer_color})
        ret["From"] = self.font_from.render(writer+":",1,writer_color)
        ret["Msg"] = self.font_msg.render(msg,1,(0,0,0))
        ret["X From"] = 0
        ret["X Msg"] = 0 + ret["From"].get_size()[0]+3
        if ret["X Msg"] + ret["Msg"].get_size()[0] > self.size[0]:
            palabras = []
            palabra_actual = ""
            for x in range(len(msg)):
                if msg[x] == " ":
                    palabras.append(palabra_actual)
                    palabra_actual = ""
                else:
                    palabra_actual += msg[x]
            if palabra_actual != "":
                palabras.append(palabra_actual)
            ret["Msg"] = []
            actual_x = ret["X Msg"]
            inicio_linea = 0
            for x in range(len(palabras)):
                rend = self.font_msg.render(palabras[x]+" ",1,(0,0,0))
                actual_x += rend.get_size()[0]
                if actual_x > self.size[0]:
                    ret["Msg"].append(self.__GenerateRenderByWord(palabras,inicio_linea,x-1))
                    inicio_linea = x-1
                    actual_x = rend.get_size()[0]
            if inicio_linea != len(palabras):
                    ret["Msg"].append(self.__GenerateRenderByWord(palabras,inicio_linea,len(palabras)))
        else:
            ret["Msg"] = [ret["Msg"]]
        return ret
    def __GenerateRenderByWord(self,palabras,inicial,final):
        text = ""
        for x in range(inicial,final):
            text += palabras[x]
            text += " "
        return self.font_msg.render(text,1,(0,0,0))
    def AddMessage(self,writer,msg):
        self.messages.append({"From":writer,"Msg":msg,"Render":self.GenerateRender(writer,msg)})
    def GraphicUpdate(self,screen):
        surf = self.GenerateSurface()
        screen.blit(surf,(self.x,self.y))
    def LogicUpdate(self):
        pass

class Pointer:
    def __init__(self,value):
        self.value = value

class Chat:
    def __init__(self,size,name,position,parent):
        self.screen = None

        self.analizer = PressAnalizer()

        self.size = size
        self.blitSurfaces = []

        self.parent = parent
        self.x,self.y = position

        self.enabled = False #1=I can write text, 0=I can't write text
        self.SendText = ""

        self.amountMsj = 5

        self.msj = []

        self.lastMsj = {"p":(0,0),"s":(0,0)}
        self.name = name

        self.Disable()

    def Event(self,e):
        if self.enabled:
            self.analizer.Event(e)

    def AddMessage(self,sender,message,color=(100,100,100)):
        self.msj.append({"writer":sender,"msj":message,"color":color,"p":(0,0),"s":(0,0)})
        #self.shownMsj.append({"writer":sender,"content":message})
        #self.chats_zone.AddMessage(sender,message)
    def GenerateBackground(self,color):
        self.background = pygame.Surface(self.size)
        self.background.fill(color)
        AddBorder(self.background,2)
        self.background.set_alpha(100)
    def LogicUpdate(self):
        self.analizer.SetKeys(pygame.key.get_pressed())
        if self.enabled:
            self.analizer.Update()
            self.BlitInPlace("last",0,self.name,self.analizer.GetText())

            if pygame.key.get_pressed()[K_RETURN] or pygame.key.get_pressed()[K_KP_ENTER]:
                self.parent.parent.Send({"action":"send_chat","message":self.analizer.GetText()})
                self.enabled = False
                self.analizer.ClearText()
        else:
            self.BlitInPlace("last",0,self.name,"Press T to talk")

            if pygame.key.get_pressed()[K_t]:
                self.enabled = True
        start = max(0 , len(self.msj) - self.amountMsj)
        end = len(self.msj)
        order = 0
        for item in range( start , end ):
            self.BlitInPlace(order , item , self.msj[item]["writer"] , self.msj[item]["msj"] , self.msj[item]["color"])
            order += 1


    def Enable(self):
        self.BlitInPlace("last",0,self.name,"")
    def Disable(self):
        self.BlitInPlace("last",0,self.name,"Press T to talk")
    def GraphicUpdate(self,screen):
        self.screen = screen
        for blit in self.blitSurfaces:
            screen.blit(blit["s"],blit["p"])
        self.blitSurfaces = []
    def BlitInPlace(self,item,real,writer,msj,color=(46, 65, 114)):
        if item == "last":
            self.BlitPosition((240,270),writer,msj,(46, 65, 114),self.lastMsj)
        else:
            self.BlitPosition((240,170+item*20),writer,msj,color,self.msj[real])

    def BlitPosition(self,position,writer,msj,color,oldRef):
        surface = fonts.MotionControl.c15.render(str(writer)+": "+str(msj),1,color)
        self.blitSurfaces.append({"s":surface,"p":position})

        x,y = position
        w,h = surface.get_size()

        if oldRef:
            lx , ly = oldRef["p"]
            lw , lh = oldRef["s"]
            self.parent.AddUpdateRect(lx,ly,lw,lh)

        oldRef["p"] = (x,y)
        oldRef["s"] = (w,h)

        self.parent.AddUpdateRect(x,y,w,h)