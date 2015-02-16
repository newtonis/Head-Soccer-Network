from logs import *

##### An orderUpdateList is an object that manages the access to elements and the order to update or draw them ######

def gkey(key,amount):
     if amount == 1:
         return key
     else:
         return key + "#" + str(amount)

class OrderUpdateList(Log_object):
    def __init__(self,screen):
        self.elements   = dict()
        self.keys_order = []
        self.SetScreen(screen)
    def AddElement(self,element,key,wtype = "front",amount = 1):
        finalkey = gkey(key,amount)
        if self.elements.has_key(finalkey): #if key is repeated
            return self.AddElement(element,key,amount + 1) #add the element with key increased in 1
        else:
            element.SetScreen(self.screen)
            self.elements[finalkey] = element
            if wtype == "front":
                self.keys_order.append(finalkey)
            return finalkey
    def RemoveElement(self,key):
        del self.elements[key]
        for x in range(len(self.keys_order)):
            k = self.keys_order[x]
            if k == key:
                del self.keys_order[x]
                return
    def KEYS(self):
        return self.keys_order
    def ELEMENTS(self,key):
        return self.elements[key]
    def Event(self,e):
        for k in self.KEYS():
             element = self.ELEMENTS(k)
             element.Event(e)
        self.extraEvent(e)
    def Draw(self):
        for k in self.KEYS():
             element = self.ELEMENTS(k)
             element.Draw()
        self.extraDraw()
    def UTimes(self,s):
        for k in self.KEYS():
             element = self.ELEMENTS(k)
             element.UTimes(s)
        self.extraUTimes(s)
    def extraDraw(self):
        pass
    def extraEvent(self,e): 
        pass
    def extraUTimes(self,ms):
        pass
    def SetScreen(self,screen):
        self.screen = screen
        if self.screen != None:
             self.screenWidth , self.screenHeight = self.screen.get_size()
        else:
             self.screenWidth , self.screenHeight = 0,0
        for k in self.KEYS():
            element = self.ELEMENTS()[k]
            element.SetScreen(self.screen)

class OULelement: #An element compatible with an order update list
    def __init__(self,screen):
        self.SetScreen(screen)
    def SetScreen(self,screen):
        self.screen = screen 
        if self.screen != None:
            self.screenWidth , self.screenHeight = self.screen.get_size()
        else:
            self.screenWidth , self.screenHeight = 0,0
    def Draw(self):
        pass
    def Event(self,e):
        pass
    def UTimes(self,s):   
        pass

