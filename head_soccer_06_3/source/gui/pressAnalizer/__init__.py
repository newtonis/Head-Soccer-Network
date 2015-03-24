__author__ = 'newtonis'

import pygame
import time

global LETTERS,NUMBERS,COMBINATIONS,CAPITAL_LETTERS
LETTERS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
NUMBERS = ["1","2","3","4","5","6","7","8","9","0",".","-"]
NUMBERS_EXCEPTIONS = ["-"]
COMBINATIONS = ["!","'","#","$","%","&","/","(",")","=","","?"]
CAPITAL_LETTERS = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

class PressAnalizer:
    def __init__(self):
        self.queue = []

        self.pressed_shift = False
        self.pressed_ctrl = False
        self.pressed_tab = False
        self.pressed_alt = False

        self.pressed_keys = []
        self.waiting_time = time.time()
        self.events = []
        self.keys = []
        self.lkeys = []

        self.text = ""
    def SetKeys(self,pressed):
        self.lkeys = self.keys
        self.keys = pressed
    def Update(self):
        written = ""
        keyup = ""
        for key in range(len(self.keys)):
            if not self.lkeys:
                continue
            if self.keys[key] and not self.lkeys[key]:
                act_written = pygame.key.name(key)
                self.pressed_keys.append({"Key":act_written,"Time":time.time(),"Waiting time":1})
                if act_written[0] == "[":
                    act_written = act_written[1:2]
                written = act_written
                #  Haciendo funcionar el arroba con cualquiera de los dos alt
                if self.pressed_alt and (act_written == "q" or act_written == "2") and self.special_allowed:
                    written = "@"
                    self.Write("@")
            if not self.keys[key] and self.lkeys[key]:
                keyup = pygame.key.name(key)
                for x in range(len(self.pressed_keys)):
                    if self.pressed_keys[x]["Key"] == keyup:
                        del self.pressed_keys[x]
                        break

        self.events = [] #reset events

        #  Analizando si se esta repitiendo alguna tecla
        for x in range(len(self.pressed_keys)):
            if time.time() - self.pressed_keys[x]["Time"] >= self.pressed_keys[x]["Waiting time"]:
                if written == "":
                    written = self.pressed_keys[x]["Key"]
                    self.pressed_keys[x]["Time"] = time.time()
                    self.pressed_keys[x]["Waiting time"] = .05

        #  Anotando letras y numeros segun corresponda
        for letter in range(len(LETTERS)):
            if written == LETTERS[letter]:
                if self.pressed_shift:
                    self.Write(CAPITAL_LETTERS[letter])
                else:
                    self.Write(written)
        for number in range(len(NUMBERS)):
            if written == NUMBERS[number]:
                if self.pressed_shift:
                    self.Write(COMBINATIONS[number])
                else:
                    is_exception = False
                    for exc in NUMBERS_EXCEPTIONS:
                        if exc == written:
                            is_exception = True
                    if not is_exception:
                        self.Write(written)


        if written == "space":
            self.Write(" ")
        if written == "right shift" or written == "left shift":
            self.pressed_shift = True
        if keyup == "right shift" or keyup == "left shift":
            self.pressed_shift = False

        if written == "left ctrl":
            self.pressed_ctrl = True
        if keyup == "left ctrl":
            self.pressed_ctrl = False
        if written == "backspace":
            self.text = self.text[:len(self.text)-1]
    def ClearText(self):
        self.text = ""
    def Write(self,key):
        self.text += key
    def GetText(self):
        return self.text