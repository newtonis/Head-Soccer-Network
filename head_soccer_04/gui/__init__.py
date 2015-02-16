import time

class TextInput:
    def __init__(self,position,font = pygame.font.Font(None,20),dimensions = (100,20),background = (255,255,255),backgroundFocused = (200,200,200),border = (200,200,200),borderFocused = (0,0,0),tileIntensity = 1,initialText="",textColor=(0,0,0)):
        self.text = initialText
        self.tileIntensity = tileIntensity #per second
        self.position   = position
        self.dimensions = dimensions
        self.background = background
        self.backgroundFocused = backgroundFocused
        self.border     = border
        self.borderFocused = borderFocused
        self.focused    = False
        self.textColor  = =
    def UpdateSurface(self):
        surface = pygame.surface.Surface(self.dimensions)
        surface.fill(self.CurrentBackground())
        self.AddBorder(surface)
        textShown = self.font.render(self.text,1,self.textColor)
        center = self.GetCenter(textShown.get_size())
        surface.fill(textShown,center)
    def Draw(self):
        pass
    def Loop(self):
        pass
    def KeyEvent(self,event):
        pass
    def CurrentBackground(self):
        if self.focused:
            return self.backgroundFocused
        else:
            return self.background
    def CurrentBorder(self):
        if self.focused:
            return self.borderFocused
        else:
            return self.border
    def AddBorder(self,surface):
#line(Surface, color, start_pos, end_pos)
        points = (0,0),(surface.get_size()[0],0),(surface.get_size()[0],surface.get_size()[1]),(0,surface.get_size()[1])
        pygame.draw.lines(surface,self.CurrentBorder(),1,points)
    def GetCenter(self,size):
        return self.dimensions[0]/2 - size[0]/2 , self.dimensions[1]/2 - size[1] / 2

