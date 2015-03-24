__author__ = 'ariel'

from source.gui.button import *

class Window:
    def __init__(self , title, upColor ,downColor, x=0,y=0,width=400,height=200,titleColor=(0,0,0),downAlpha=100,borderColor=(255,255,255)):
        self.titleColor = titleColor
        self.title = title
        self.upColor = upColor
        self.downColor = downColor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.elements = []
        self.references = dict()
        self.parent = None

        self.pressed = False
        self.dx = 0
        self.dy = 0
        self.enabled = False
        self.locked  = False
        self.downAlpha = downAlpha
        self.borderColor = borderColor
        self.GenerateSurface()
        self.mouseOut = False
    def SetParent(self,parent):
        self.parent = parent
    def GenerateSurface(self):
        surfaceEnd = pygame.surface.Surface((self.width,self.height+20),pygame.SRCALPHA)

        UpSurface = pygame.surface.Surface((self.width,20))
        UpSurface.fill(self.upColor)
        textTitle = fonts.PixelSplitter.c15.render(self.title,1,self.titleColor)
        UpSurface.blit(textTitle,GetCenter(UpSurface,textTitle))

        AddBorder(UpSurface,1,self.borderColor)

        DownSurface = pygame.surface.Surface((self.width,self.height))
        DownSurface.fill(self.downColor)
        DownSurface.set_alpha(self.downAlpha)
        #AddBorder(DownSurface)

        surfaceEnd.blit(UpSurface,(0,0))
        surfaceEnd.blit(DownSurface,(0,20))
        SpecialAddBorder(surfaceEnd,[ [(0,19),(0,18+self.height)] , [(1,19+self.height),(self.width-2,19+self.height)] ,[(self.width-1,18+self.height),(self.width-1,19)] ] ,self.borderColor)

        self.surface = surfaceEnd
    def LogicUpdate(self):
        if not self.pressed and not self.mouseOut:
            self.mouseOut = True
        if not self.mouseOut:
            return

        for element in self.elements:
            element.enabled = self.enabled
            element.LogicUpdate()
        if self.pressed:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            if not self.locked:
                self.x = mouse_x - self.dx
                self.y = mouse_y - self.dy
        self.ExtraLogicUpdate()
    def ExtraLogicUpdate(self):
        pass
    def GraphicUpdate(self,screen):
        blitSurface = pygame.surface.Surface((self.width,self.height+20),pygame.SRCALPHA)
        blitSurface.blit(self.surface,(0,0))
        for element in self.elements:
            element.GraphicUpdate(blitSurface)
        screen.blit(blitSurface,(self.x,self.y))

    def AddUpdateRect(self,x,y,w,h):
        self.parent.AddUpdateRect(self.x + x,self.y + y,w,h)
    def AddElement(self,element,reference="NoReference"):
        element.SetParent(self)
        self.elements.append(element)
        if reference != "NoReference":
            return self.SetReference(element,reference)
    def DeleteElement(self,id):
        if not self.references.has_key(id):
            return
        for x in range(len(self.elements)):
            if self.elements[x] == self.references[id]:
                del self.elements[x]
                del self.references[id]
                return
    def DeleteAllElements(self):
        references =  []
        for r in self.references:
            references.append(r)
        for ref in references:
            self.DeleteElement(ref)
    def SetReference(self,element,reference,value=1):
        if value != 1:
            reference += "#"+str(value)
        if self.references.has_key(reference):
            return self.SetReference(element,reference,value+1)
        else:
            self.references[reference] = element
            return reference
    def MouseClickIn(self,mouse_x,mouse_y):
        if mouse_x >= self.x and mouse_x < self.x + self.width:
            if mouse_y >= self.y and mouse_y < self.y + 25:
                self.pressed = True
                self.dx = mouse_x - self.x
                self.dy = mouse_y - self.y
                return True
        return False

    def MouseIsInto(self,mouse_x,mouse_y):
        if mouse_x >= self.x and mouse_x < self.x + self.width:
            if mouse_y >= self.y and mouse_y < self.y + 25 + self.height:
                return True
        return False
    def Event(self,e):
        for element in self.elements:
            element.Event(e)
    def Kill(self):
        self.parent.Kill(self)
    def Centralize(self):
        self.x = self.parent.screen.get_size()[0]/2 - self.width/2
        self.y = self.parent.screen.get_size()[1]/2 - self.height/2
    def ButtonCheck(self,id):
        if self.references.has_key(id):
            if self.references[id].pressed:
                return True
        return False
    def SetWidth(self,width):
        self.width = width
        self.GenerateSurface()
    def SetHeight(self,height):
        self.height = height
        self.GenerateSurface()
    def SetSize(self,size):
        self.width,self.height = size
        self.GenerateSurface()

class TestWindow(Window):
    def __init__(self,px=0,py=0):
        Window.__init__(self,title="Test Window",x=px,y=py,upColor=(84, 160, 224),downColor=(255, 209, 72))
        self.AddElement(ClassicButton("close",(200,200,200),(20,20)))