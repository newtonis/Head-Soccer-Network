__author__ = 'Dylan'

import pygame
from source.gui.element import Element
from source.gui.RoundedCorners import CircleBorderRectangle
from source.gui.pyperclip import copy,paste
from source.data.fonts import *
from pygame.locals import *
import time
import copy

global LETTERS,NUMBERS,COMBINATIONS,CAPITAL_LETTERS
LETTERS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
NUMBERS = ["1","2","3","4","5","6","7","8","9","0",".","-"]
NUMBERS_EXCEPTIONS = ["-"]
COMBINATIONS = ["!","'","#","$","%","&","/","(",")","=","","?"]
CAPITAL_LETTERS = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

class Input(Element):
    def __init__(self):
        Element.__init__(self,(0,0))
        self.background_color = (255,255,255)
        self.corner_exceptions = [0,1,2,3]
        self.radius = 10
        self.size = (200,30)
        self.border_size = 2
        self.border_color = (0,0,0)
        self.opacity = 255
        self.font_color = (0,0,0)
        self.background = None
        self.font = None
        self.GenerateBackground()
        self.original_font = BebasNeue
        self.GenerateFont(self.original_font)
        self.text = ""
        self.x = 0
        self.y = 0
        self.selected = False
        self.cursor = {"Image":pygame.Surface((2,self.size[1]-10)),"Letter":0,"Enabled":False,"Time":time.time()}
        self.separation = 8
        self.letters_allowed = False
        self.numbers_allowed = False
        self.special_allowed = False
        self.events = []
        self.pressed_shift = False
        self.pressed_ctrl = False
        self.pressed_tab = False
        self.pressed_alt = False
        self.text_data = {"Locked in":"Left", "Difference":0, "Position":[0,0]}
        self.pressed_keys = []
        self.waiting_time = time.time()
        self.selection = {"Selecting":False,"Mouse pressed":-1,"Start":0,"End":0}
        self.next_input = None
        self.password = False
    def SetBackgroundColor(self,r,g,b):
        self.background_color = (r,g,b)
        self.GenerateBackground()
    def SetBackgroundRoundedCorners(self,top_left,top_right,down_left,down_right,radius):
        self.corner_exceptions = []
        if top_left:
            self.corner_exceptions.append(0)
        if top_right:
            self.corner_exceptions.append(1)
        if down_left:
            self.corner_exceptions.append(2)
        if down_right:
            self.corner_exceptions.append(3)
        self.radius = radius
        self.GenerateBackground()
    def SetSize(self,w,h):
        self.size = (w,h)
        self.GenerateFont(self.original_font)
        self.GenerateBackground()
        self.cursor["Image"] = pygame.Surface((2,self.size[1]-10))
    def SetBorderSize(self,border_size):
        self.border_size = border_size
        self.GenerateBackground()
    def SetBorderColor(self,border_color):
        self.border_color = border_color
        self.GenerateBackground()
    def SetBackgroundOpacity(self,opacity):
        self.opacity = opacity
        self.GenerateBackground()
    def SetTextColor(self,r,g,b):
        self.font_color = (r,g,b)
        self.GenerateBackground()
    def SetNextInput(self,pointer):
        self.next_input = pointer
    def AllowLetters(self):
        self.letters_allowed = True
    def AllowNumbers(self):
        self.numbers_allowed = True
    def AllowSpecialCharacters(self):
        self.special_allowed = True
    def AllowAll(self):
        self.letters_allowed = True
        self.numbers_allowed = True
        self.special_allowed = True
    def GenerateBackground(self):
        self.background = CircleBorderRectangle(self.size,self.border_color,self.radius,False,0,self.opacity,self.corner_exceptions)
        border = CircleBorderRectangle([self.size[0]-2*self.border_size,self.size[1]-2*self.border_size],self.background_color,self.radius,False,1,self.opacity,self.corner_exceptions)
        self.background.blit(border,(self.border_size,self.border_size))
    def GenerateFont(self,font):
        sizes = []
        for x in range(len(font.array)):
            test = font.array[x].render("HOLA",1,(0,0,0))
            test_size = test.get_size()
            sizes.append(test_size[1])
        self.font = font.array[len(font.array)-1]
        rad = self.radius*2
        if self.corner_exceptions == [0,1,2,3]:
            rad = 2*self.border_size
        for x in range(len(sizes)-1):
            if sizes[x] < self.size[1]-rad and sizes[x+1] > self.size[1]-rad:
                self.font = font.array[x]
    def Event(self,e):
        self.events = e
    def Write(self,text):
        if self.selection["Start"] != 0:
            self.DeleteSelection()
        self.text = self.text[:self.cursor["Letter"]]+text+self.text[self.cursor["Letter"]:]
        self.MoveCursorRight()
    def MoveCursorRight(self):
        self.cursor["Letter"] += 1
        if self.cursor["Letter"] >= len(self.text):
            self.cursor["Letter"] = len(self.text)
        if self.text_data["Locked in"] == "Right" and self.text_data["Difference"] > 0:
            self.text_data["Difference"] -= 1
    def MoveCursorLeft(self):
        self.cursor["Letter"] -= 1
        if self.cursor["Letter"] <= 0:
            self.cursor["Letter"] = 0
        if self.text_data["Locked in"] == "Left" and self.text_data["Difference"] > 0:
            self.text_data["Difference"] -= 1
    def AnalizeWritten(self):
        global LETTERS,NUMBERS,COMBINATIONS,CAPITAL_LETTERS,NUMBERS_EXCEPTIONS
        """  Detectando escritura  """
        written = ""
        keyup = ""
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                act_written = pygame.key.name(event.key)
                self.pressed_keys.append({"Key":act_written,"Time":time.time(),"Waiting time":1})
                if act_written[0] == "[":
                    act_written = act_written[1:2]
                written = act_written
                """  Haciendo funcionar el arroba con cualquiera de los dos alt  """
                if self.pressed_alt and (act_written == "q" or act_written == "2") and self.special_allowed:
                    written = "@"
                    self.Write("@")
            if event.type == pygame.KEYUP:
                keyup = pygame.key.name(event.key)
                for x in range(len(self.pressed_keys)):
                    if self.pressed_keys[x]["Key"] == keyup:
                        del self.pressed_keys[x]
                        break
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.selection["Mouse pressed"] = self.GetMouse()[0]
            if event.type == pygame.MOUSEBUTTONUP:
                if not self.selection["Selecting"]:
                    self.selection["Start"] = 0
                    self.selection["End"] = 0
                self.selection["Mouse pressed"] = -1
        self.events = []
        """  Analizando si se esta repitiendo alguna tecla  """
        for x in range(len(self.pressed_keys)):
            if time.time() - self.pressed_keys[x]["Time"] >= self.pressed_keys[x]["Waiting time"]:
                if written == "":
                    written = self.pressed_keys[x]["Key"]
                    self.pressed_keys[x]["Time"] = time.time()
                    self.pressed_keys[x]["Waiting time"] = .05
        """  Analizando si lo detectado esta dentro de los caracteres permitidos  """
        if self.letters_allowed:
            for letter in range(len(LETTERS)):
                if written == LETTERS[letter]:
                    if self.pressed_shift:
                        self.Write(CAPITAL_LETTERS[letter])
                    else:
                        if self.pressed_ctrl and (written == "c" or written == "v"):
                            if written == "c":
                                if self.selection["Start"] != 0:
                                    start,end = self.selection["Start"],self.selection["End"]
                                    if self.selection["End"]-self.selection["Start"] < 0:
                                        start = end
                                        end = self.selection["Start"]
                                    copy(self.text[start:end])
                            elif written == "v":
                                text_to_add = paste()
                                for x in text_to_add:
                                    self.Write(x)
                        else:
                            self.Write(written)
        if self.numbers_allowed:
            for number in range(len(NUMBERS)):
                if written == NUMBERS[number]:
                    if self.pressed_shift:
                        if self.special_allowed:
                            self.Write(COMBINATIONS[number])
                    else:
                        is_exception = False
                        for exc in NUMBERS_EXCEPTIONS:
                            if exc == written:
                                is_exception = True
                        if not is_exception:
                            self.Write(written)
        """  Analizando si se presiono algun caracter especial como shift,espacio,etc  """
        if written == "space":
            self.Write(" ")
        if written == "right shift" or written == "left shift":
            self.pressed_shift = True
        if keyup == "right shift" or keyup == "left shift":
            self.pressed_shift = False
        if written == "backspace":
            if self.selection["Start"] == 0:
                self.text = self.text[:self.cursor["Letter"]-1]+self.text[self.cursor["Letter"]:]
                self.MoveCursorLeft()
            else:
                self.DeleteSelection()
        if written == "left ctrl":
            self.pressed_ctrl = True
        if keyup == "left ctrl":
            self.pressed_ctrl = False
        if written == "tab":
            self.pressed_tab = True
        if keyup == "tab" and self.pressed_tab:
            self.pressed_tab = False
            if self.next_input != None:
                self.pressed_keys = []
                self.selected = False
                self.next_input.selected = True
        if written == "right alt" or written == "left alt":
            self.pressed_alt = True
        if keyup == "right alt" or keyup == "left alt":
            self.pressed_alt = False
        """  Analizando si se presionan las flechas para mover el cursor  """
        if written == "left":
            if self.selection["Start"] == 0:
                self.MoveCursorLeft()
            else:
                self.selection["Start"],self.selection["End"] = 0,0
                if not (self.selection["End"]-self.selection["Start"] < 0):
                    for x in range(self.selection["End"]-self.selection["Start"]):
                        self.MoveCursorLeft()
        if written == "right":
            if self.selection["Start"] == 0:
                self.MoveCursorRight()
            else:
                self.selection["Start"],self.selection["End"] = 0,0
                if self.selection["End"]-self.selection["Start"] < 0:
                    for x in range(self.selection["Start"]-self.selection["End"]):
                        self.MoveCursorRight()
    def CursorTics(self):
        if time.time() > self.cursor["Time"]+.3:
            self.cursor["Time"] = time.time()
            if self.cursor["Enabled"]:
                self.cursor["Enabled"] = False
            else:
                self.cursor["Enabled"] = True
    def CalculateTextData(self):
        text_width = self.size[0] - 2*self.separation
        if self.text_data["Locked in"] == "Left":
            test = self.font.render(self.text[self.text_data["Difference"]:self.cursor["Letter"]],1,(0,0,0))
            if test.get_size()[0] > text_width:
                self.text_data["Locked in"] = "Right"
                self.text_data["Difference"] = len(self.text) - self.cursor["Letter"]
        else:
            test = self.font.render(self.text[self.cursor["Letter"]:len(self.text)-self.text_data["Difference"]],1,(0,0,0))
            if test.get_size()[0] > text_width:
                self.text_data["Locked in"] = "Left"
                self.text_data["Difference"] = self.cursor["Letter"]
            test2 = self.font.render(self.text,1,(0,0,0))
            if test2.get_size()[0] < text_width:
                self.text_data["Locked in"] = "Left"
                self.text_data["Difference"] = 0
    def CalculateNearestPosition(self,x):
        text_real_position = self.x + self.separation + self.text_data["Position"][0]
        for w in range(len(self.text)):
            act_size = self.font.render(self.text[:w],1,(0,0,0)).get_size()[0]
            next_size = self.font.render(self.text[:w+1],1,(0,0,0)).get_size()[0]
            if text_real_position + act_size < x and text_real_position + next_size >= x:
                return w+1
        act_size = self.font.render(self.text[:len(self.text)-1],1,(0,0,0)).get_size()[0]
        if x > text_real_position + act_size:
            return len(self.text)
        return 0
    def CalculateSeleccion(self,mouse_x):
        if self.selection["Mouse pressed"] != -1:
            if mouse_x < self.selection["Mouse pressed"]-1 or mouse_x > self.selection["Mouse pressed"]+1:
                self.selection["Selecting"] = True
                self.selection["Start"] = self.CalculateNearestPosition(self.selection["Mouse pressed"])
                self.selection["End"] = self.CalculateNearestPosition(self.selection["Mouse pressed"])
            if self.selection["Selecting"]:
                self.selection["End"] = self.CalculateNearestPosition(mouse_x)
        else:
            self.selection["Selecting"] = False
    def DeleteSelection(self):
        if self.selection["End"]-self.selection["Start"] < 0:
            start = self.selection["End"]
            end = self.selection["Start"]
        else:
            start = self.selection["Start"]
            end = self.selection["End"]
            for x in range(end - start):
                self.MoveCursorLeft()
        self.selection["Start"],self.selection["End"] = 0,0
        self.text = self.text[:start]+self.text[end:]
    def GraphicUpdate(self,screen):
        background_copy = pygame.Surface.copy(self.background)
        """  Creando text_surface que es el surface que va a contener el texto y la seleccion  """
        rad = 2*self.radius
        if self.corner_exceptions == [0,1,2,3]:
            rad = 2*self.border_size
        text_surface = pygame.Surface((self.size[0]-2*self.separation,self.size[1]-rad))
        """  Dibujando texto escrito en el text_surface  """
        text_surface.fill(self.background_color)
        """  Password  """
        text = copy.copy(self.text)
        if self.password:
            text = ""
            for x in range(len(self.text)):
                text += "x"
        """  Generating render  """
        render = self.font.render(text,1,self.font_color)
        if self.text_data["Locked in"] == "Left":
            difference = self.font.render(self.text[:self.text_data["Difference"]],1,(0,0,0)).get_size()[0]
            text_pos = (-difference,text_surface.get_size()[1]/2-render.get_size()[1]/2)
        else:
            difference = self.font.render(self.text[len(self.text)-self.text_data["Difference"]:],1,(0,0,0)).get_size()[0]
            text_pos = (text_surface.get_size()[0]-render.get_size()[0]+difference,text_surface.get_size()[1]/2-render.get_size()[1]/2)
        self.text_data["Position"] = text_pos
        text_surface.blit(render,text_pos)
        """  Dibujando seleccion en la pantalla  """
        selection_width = self.font.render(self.text[self.selection["Start"]:self.selection["End"]],1,(0,0,0))
        start_letter = self.selection["Start"]
        if self.selection["End"]-self.selection["Start"] < 0:
            selection_width = self.font.render(self.text[self.selection["End"]:self.selection["Start"]],1,(0,0,0))
            start_letter = self.selection["End"]
        start_pos = self.font.render(self.text[:start_letter],1,(0,0,0)).get_size()[0]
        selection_surface = pygame.Surface((selection_width.get_size()[0],self.cursor["Image"].get_size()[1]))
        selection_surface.fill((0,162,255))
        selection_surface.set_alpha(100)
        if self.selection["Start"] != 0 and self.selected:
            text_surface.blit(selection_surface,(text_pos[0]+start_pos,text_surface.get_size()[1]/2-self.cursor["Image"].get_size()[1]/2))
        """  Dibujando el text_surface en la pantalla  """
        background_copy.blit(text_surface,(self.separation,rad/2))
        """  Dibujando el cursor en la pantalla  """
        cursor_pos = [
            self.font.render(text[:self.cursor["Letter"]],1,(0,0,0)).get_size()[0] + self.separation + text_pos[0],
            5
        ]
        if self.cursor["Enabled"] and self.selected:
            background_copy.blit(self.cursor["Image"],cursor_pos)

        """  Dibujando input en la pantalla  """
        screen.blit(background_copy,(self.x,self.y))
    def LogicUpdate(self):
        mouse_x,mouse_y = self.GetMouse()
        """  Comprobando si se hace click sobre la input para seleccionarla  """
        if self.GetPressed() and not self.selection["Selecting"]:
            if mouse_x > self.x and mouse_x < self.x+self.size[0] and mouse_y > self.y and mouse_y < self.y+self.size[1]:
                self.selected = True
            else:
                self.selected = False
        """  Si la input esta seleccionada va a realizar toda la logica  """
        if self.selected:
            self.AnalizeWritten()
            self.CursorTics()
            self.CalculateTextData()
            self.CalculateSeleccion(mouse_x)
            if self.GetPressed():
                if mouse_x > self.x and mouse_x < self.x+self.size[0] and mouse_y > self.y and mouse_y < self.y+self.size[1]:
                    self.cursor["Letter"] = self.CalculateNearestPosition(mouse_x)
                    if time.time() - self.waiting_time >= .1:
                        if mouse_x < self.x + self.separation:
                            self.MoveCursorLeft()
                        if mouse_x > self.x + self.size[0] - self.separation:
                            self.MoveCursorRight()
                        self.waiting_time = time.time()
