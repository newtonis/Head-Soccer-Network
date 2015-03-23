__author__ = 'Dylan'

import pygame
from pygame.locals import *
from source.gui.addBorder import AddBorder
from source.gui.input import Input
from source.data.fonts import *
from source.data.images import Extras
from source.gui.bar import Bar
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


class Chat:
    def __init__(self,size,background,position,parent):
        global font
        self.visible = True
        self.size = size
        self.background = None
        self.parent = parent
        self.x,self.y = position
        self.GenerateBackground(background)
        self.input = Input()
        self.input.AllowAll()
        self.input.SetSize(self.size[0],25)
        self.input.SetBackgroundColor(0,0,255)
        self.input.SetTextColor(0,255,0)
        self.input.x = 0
        self.input.y = self.size[1]-self.input.size[1]
        self.input.SetParent(self)
        self.input.GenerateFont(font)
        self.input.GenerateBackground()
        self.chats_zone = MsgBox((self.size[0]-10,self.size[1]-10-self.input.size[1]),(self.x+5,self.y+5),self)
        self.recently_pressed = False
    def AddMessage(self,sender,message):
        self.chats_zone.AddMessage(sender,message)
    def GenerateBackground(self,color):
        self.background = pygame.Surface(self.size)
        self.background.fill(color)
        AddBorder(self.background,2)
        self.background.set_alpha(100)
    def LogicUpdate(self):
        self.input.Event(self.parent.parent.events)
        self.input.LogicUpdate()
        self.chats_zone.LogicUpdate()
        if pygame.key.get_pressed()[K_RETURN] or pygame.key.get_pressed()[K_KP_ENTER]:
            if not self.recently_pressed and self.input.selected:
                self.recently_pressed = True
                self.parent.parent.Send({"action":"send_chat","message":self.input.text})
                self.input.text = ""
        else:
            self.recently_pressed = False
    def GraphicUpdate(self,screen):
        if self.visible:
            back = self.background.copy()
            self.input.GraphicUpdate(back)
            self.chats_zone.GraphicUpdate(screen)
            screen.blit(back,(self.x,self.y))