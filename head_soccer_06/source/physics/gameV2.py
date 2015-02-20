__author__ = 'newtonis'

#################### Game ########################
#                                                #
# This file is used by both, the client and the  #
# server. Here is controlled all the game engine #
# using the library Box2D, also control the goal #
# animation.                                     #
#                                                #
##################################################

################## Imports ######################
import contactListener as contactL              #
import pygame                                   #
import Box2D                                    #
import time                                     #
from PodSixNet.Server import Server             #
from PodSixNet.Channel import Channel           #
from PodSixNet.ServerUDP import ServerUDP       #
from source.gui import container                #
from source.data import fonts                   #
from source.data import config                  #
from source.data.images import *                #
from source.gui.surface import *                #
from Box2D.b2 import *                          #
#################################################

### This layers are used to determinate which object collide with which other ###
LAYER_1 = 0x0001                                                              ###
LAYER_2 = 0x0002                                                              ###
LAYER_3 = 0x0004                                                              ###
LAYER_4 = 0x0008                                                              ###
#################################################################################

def my_draw_polygon(polygon, body, fixture , handler ,color ,screen):
    vertices=[(body.transform*v)*handler.PPM for v in polygon.vertices]
    vertices=[(v[0], handler.pixelHeight-v[1]) for v in vertices]
    pygame.draw.polygon(screen, color, vertices)
polygonShape.draw=my_draw_polygon

def my_draw_circle(circle, body, fixture , handler ,color ,screen):
    position=body.transform*circle.pos*handler.PPM
    position=(position[0], handler.pixelHeight-position[1])
    pygame.draw.circle(screen, color, [int(x) for x in position], int(circle.radius*handler.PPM))
circleShape.draw=my_draw_circle

def dd(value):
    """
    :param value: string value to convert
    :return:      value converted to two characters string
    """
    value = int(value)
    if value < 10:
        return "0"+str(value)
    else:
        return value

def rr05(value):
    """ This function converts box2D position or linear velocity array to classic array
    :param value: Position of type box2d array
    :return:      Converted value to normal array
    """
    return value[0] , value[1]

def BoomBox(letter,color=(100,100,200),font="Classic"):
    """ This function generate render with font Box2D
    :param letter: Text to render
    :param color:  Color of render
    :param font:   Size of render
    :return:       Rendered text
    """
    if font == "Classic": # Render with size 80
        font = fonts.BoomBox.NewVersion.c80
    elif font == "Boombox60": # Render with size 60
        font = fonts.BoomBox.Original.c60
    elif font == "Boombox40": # Render with size 40
        font = fonts.BoomBox.Original.c40
    elif font == "Boombox20": # Render with size 20
        font = fonts.BoomBox.NewVersion.c20
    surface = font.render(letter,1,color) # Generate render
    return surface

###  Single letter of the goal animation  ###
class AnimationLetter:
    def __init__(self,letter,final_position,actual_position,loops,color=(100,100,200),font="Classic"):
        """
        :param letter:          Letter to blit
        :param final_position:  Position where the animation will finish
        :param actual_position: Position where the animation starts
        :param loops:           The number of loop the animation will continue
        :param color:           Color of the letter
        :param font:            Size of the font
        """
        self.letter = letter
        self.surface = BoomBox(letter,color,font) # Generating render
        self.sx,self.sy = actual_position[0],actual_position[1] # Saving the start position
        self.x,self.y = actual_position[0],actual_position[1] # Setting actual position
        self.lx,self.ly = final_position[0],final_position[1] # Saving last position to compare every loop
        self.loops = loops
        self.loop = 0 # Loop counter
    def GraphicUpdate(self,screen):
        """
        :param screen: Pygame surface of the screen
        """
        screen.blit(self.surface,(self.x,self.y)) # Blitting surface to the screen in actual position
    def Size(self):
        """
        :return: Size of the surface of the letter
        """
        return self.surface.get_size()
    def Width(self):
        """
        :return: Width of the surface
        """
        return self.surface.get_size()[0]
    def Heigth(self):
        """
        :return: Height of the surface
        """
        return self.surface.get_size()[1]
    def LogicUpdate(self):
        self.loop += 1 # Loop increments in one every loop
        if self.loop > self.loops: # Compare if animation if finished
            return
        x_variant = self.lx - self.sx # This variable is the total x route of the animation
        y_variant = self.ly - self.sy # This variable is the total y route of the animation

        x_value = x_variant * float(float(self.loop)/float(self.loops)) # There is the route traveled in x since start
        y_value = y_variant * float(float(self.loop)/float(self.loops)) # There is the route traveled in y since start

        self.x = self.sx + x_value # Setting new x to start x plus x_value
        self.y = self.sy + y_value # Setting new y to start y plus y_value
    def Reverse(self):
        ### Start animation from end position ###
        self.loop = 0 # Restart loops
        gx = self.sx # Save initial x
        gy = self.sy # Save initial y
        self.sx = self.lx # Set initial x to actual x
        self.sy = self.ly # Set initial y to actual y
        self.lx = gx # Set last x to saved start x
        self.ly = gy # Set last y to saved start y

###  Generate goal animation  ###
class LettersAnimation:
    def __init__(self,msj,color,parent,duration,font):
        """
        :param msj:      String with the text of animation
        :param color:    Color of the text render
        :param parent:   Parent usually is PowerGameEngine instance to use if we need some functions
        :param duration: Count of loops of duration of the animation
        :param font:     Font to be used in the render of the text
        """
        self.parent = parent
        self.letters = [] # Generate array of letters
        self.sum_width = 0
        self.loops = duration
        self.letterSeparation = 20 # Count of pixel separation between letters

        for letter in msj: # Separating letters in an array
            self.letters.append(AnimationLetter(letter,(0,0),(0,0),self.loops,color,font)) # Generating render of letter and inserting into array
            self.sum_width += self.letters[-1].Width() + self.letterSeparation
            self.height = self.letters[-1].Heigth()
        letters_per_side = len(msj) / 4 # Count of letters to move in block
        rest = len(msj) % 4 # Rest of letters if division have rest
        self.start_x = parent.pixelWidth/2 - self.sum_width / 2 # Set initial x to center of the screen
        self.start = 0 # Letter start
        self.x_st = self.start_x # Set actual x to initial x
        self.Set(0,letters_per_side) # Set letter 0
        self.Set(1,letters_per_side) # Set letter 1
        self.Set(2,letters_per_side) # Set letter 2
        self.Set(3,letters_per_side+rest) # Set letter 3
        self.loop = 0 # Loop counter
    def Set(self,letter,amount):
        pos = [(-200,-200),(-200,200),(self.parent.pixelWidth,self.parent.pixelHeight),(self.parent.pixelWidth,-200)] # All letters start position
        y_pos = self.parent.pixelHeight/2 - self.height/2 # Y pos set to the center of the screen

        for x in range(self.start,self.start+amount): # For arround actual letter block
            self.letters[x].sx , self.letters[x].sy = pos[letter] # Setting initial position of block
            self.letters[x].lx , self.letters[x].ly = self.x_st , y_pos # Setting end position of block
            self.x_st += self.letters[x].Width() + self.letterSeparation # Adding letter size and letter separation to actual x
        self.start += amount # Moving start letter to next block
    def LogicUpdate(self):
        self.loop += 1 # Loop counter
        for letter in self.letters: # Logic update for letters
            letter.LogicUpdate()
    def GraphicUpdate(self,screen):
        for letter in self.letters: # Graphic update for letters
            letter.GraphicUpdate(screen)
    def Reverse(self):
        self.loop = 0 # Restarting loops
        for letter in self.letters:
            letter.Reverse() # Restarting data of every letter
    def EndLoop(self):
        return self.loop >= self.loops # Get if process is finished

class LetterSystem:
    def __init__(self,parent):
        self.parent = parent
        self.CurrentAnimation = None
        #self.nextAnimation = None
        self.autoRemove = False
        self.status = "noAnimation"
    def LogicUpdate(self):
        if not self.CurrentAnimation:
            return
        self.CurrentAnimation.LogicUpdate()
        if self.status == "Starting":
            if self.CurrentAnimation.EndLoop() and self.waitTime != -1:
                self.status = "WaitingExit"
                self.waitRef = time.time() * 1000
        elif self.status == "WaitingExit":
            if time.time() * 1000 - self.waitRef > self.waitTime * 1000:
                self.RemoveWord()
        elif self.status == "Ending":
            if self.CurrentAnimation.EndLoop():
                self.CurrentAnimation = None
    def GraphicUpdate(self,screen):
        if self.CurrentAnimation:
            self.CurrentAnimation.GraphicUpdate(screen)
    def AddWord(self,word,color,time,font,autoRemoveTime=3):
        self.CurrentAnimation = LettersAnimation(word,color,self.parent,time,font)
        self.waitTime = autoRemoveTime
        self.status = "Starting"
    def RemoveWord(self): ### CALLED IN CASE autoRemoveTime=-1
        self.CurrentAnimation.Reverse()
        self.status = "Ending"
    def EndLoop(self):
        if not self.CurrentAnimation:
            return False
        return self.CurrentAnimation.EndLoop()

class ScoreSystem(container.Container):
    def __init__(self,parent):
        container.Container.__init__(self)
        self.parent = parent
        self.scoreA = 0
        self.scoreB = 0
        self.letterSys = None
        self.ChangeStatus("disabled")
        self.args = None
        self.new_flag = False
        self.color = (0,0,0)
    def SetLetterSystem(self,system):
        self.letterSys = system
    def LogicUpdate(self):
        container.Container.LogicUpdate(self)
        if self.args != None:
            if not self.Ereferences.has_key("Score "+self.args):
                self.status = "disabled"

        if self.status == "disabled":
            pass
        elif self.status == "normal":
            pass
        elif self.status == "goal_change":
            if self.new_flag:
                self.letterSys.AddWord("GOAL",(100,100,200),20,"Classic",-1)
            if self.letterSys.EndLoop():
                self.ChangeStatus("score_back")
        elif self.status == "score_back":
            self.Ereferences["Score "+self.args].y -= 3
            if self.Ereferences["Score "+self.args].y < -100:
                self.ChangeStatus("score_change")
                self.Ereferences["Score "+self.args].y = -100
        elif self.status == "score_change":
            self.UpdateScore(self.args,-100)
            self.ChangeStatus("score_return")
        elif self.status == "score_return":
            self.Ereferences["Score "+self.args].y += 3
            if self.Ereferences["Score "+self.args].y > 20:
                self.Ereferences["Score "+self.args].y = 20
                self.letterSys.RemoveWord()
                self.ChangeStatus("normal")
        if self.new_flag:
            self.new_flag = False
    def ChangeStatus(self,status):
        self.status = status
        self.new_flag = True
    def GraphicUpdate(self,screen):
        container.Container.GraphicUpdate(self,screen)
    def SetScore(self,letter,score):
        if letter == "A":
            self.scoreA = score
            self.ChangeStatus("goal_change")
            self.args = "A"
        if letter == "B":
            self.scoreB = score
            self.ChangeStatus("goal_change")
            self.args = "B"
    def Enable(self):
        self.status = "normal"
        self.scoreA = 0
        self.scoreB = 0
        self.AddSurfaces()
    def Disable(self):
        self.enabled = False
        self.RemoveSurfaces()
    def AddSurfaces(self):
        self.UpdateScore("A")
        self.UpdateScore("B")
        self.AddBar()
    def RemoveSurfaces(self):
        self.Delete("Score A")
        self.Delete("Score B")
        self.Delete("Bar")
    def UpdateScore(self,letter,y=20):
        self.Delete("Score "+str(letter))
        text = fonts.BebasNeue.c60.render(str(self.GetScore(letter)),1,self.color)

        positions = self.parent.pixelWidth/2-30-text.get_size()[0] , self.parent.pixelWidth/2+30
        if letter == "A":
            pos = positions[0]
        else:
            pos = positions[1]

        score = Surface(text,(pos,y))
        self.Add(score,"Score "+str(letter))
    def AddBar(self):
        self.Delete("Bar")
        text = fonts.BebasNeue.c60.render(str("-"),0,self.color)
        surface = Surface(text,(self.parent.pixelWidth/2-9,20))
        self.Add(surface,"Bar")
    def GetScore(self,letter):
        if letter == "A":
            return self.scoreA
        elif letter == "B":
            return self.scoreB

class ClockSystem:
    def __init__(self,duration,parent):
        self.parent = parent
        self.duration = duration
        self.time = 0
        self.ref_start = 0
        self.ref_stop  = 0
        self.status = "stop"
        self.play = False
        self.enabled = False
        self.graphic = False
        self.surface = None
        self.autoStop = []
        self.names = []
        self.nextStop = 0
        self.AddStop(45,"half")
        self.AddStop(90,"final")
    def AddStop(self,time,name):
        self.autoStop.append(time)
        self.names.append(name)
    def NextStop(self):
        if self.nextStop >= len(self.names):
            return None
        return {"time":self.autoStop[self.nextStop],"name":self.names[self.nextStop]}
    def Play(self):
        self.status = "play"
        if self.nextStop >= len(self.autoStop):
            print "cannot play"
            return
        self.ref_start += time.time() * 1000 - self.ref_stop
        self.play = True
    def Stop(self,s=True,instant=-1):
        self.play = False
        print instant
        if instant != -1:
            self.ref_start = time.time() * 1000 - self.DurationToPastTime(instant) * 60 * 1000
            self.UpdateTime()
            self.UpdateSurface()
        self.ref_stop = time.time() * 1000
        if s:
            self.status = "stop"
    def Reset(self):
        print "reset"
        self.nextStop = 0
        self.ref_start = 0
        self.ref_stop = 0
    def UpdateTime(self):
        time_from_start = time.time() * 1000 - self.ref_start
        max_time = 90
        duration = self.duration * 1000 * 60
        new_time = (float(time_from_start) / float(duration) )  * max_time
        nStop = self.NextStop()
        if nStop:
            if new_time > nStop["time"]:
                self.time = nStop["time"]
                self.status = nStop["name"]
                self.nextStop += 1
                self.Stop(False)
            else:
                self.time = new_time
        else:
            self.time = new_time
    def DurationToPastTime(self,time):
        return float(time) / 90.0 * self.duration
    def LogicUpdate(self):
        if self.play and self.enabled:
            self.UpdateTime()
    def GraphicUpdate(self,screen):
        if not self.enabled:
            return
        if not self.graphic:
            return
        if not self.surface:
            return
        self.surface.GraphicUpdate(screen)
    def UpdateSurface(self):
        seconds = dd(self.time)
        minutes = dd ( ( float(self.time) - int(self.time) )* 100 )

        text = fonts.Absender.c40.render(str(seconds)+":"+str(minutes),1,(0,0,0))
        self.surface = Surface(text,(self.parent.pixelWidth/2-text.get_size()[0]/2,100))
    def Enable(self):
        self.enabled = True
    def Disable(self):
        self.enabled = False
        self.Reset()
    def EnableGraphic(self):
        self.graphic = True
    def DisableGraphic(self):
        self.graphic = False
    def GetStatus(self):
        return self.status

class Element:
    def __init__(self,handler):
        self.handler = handler
        self.body = None
        self.type = "DefaultElement"
        self.parent = None
        self.last_positions = dict()
        self.freeze = False
        self.IntEnb = True
        #self.listGoTo = []
    def SetMask(self,cat,mask):
        #self.body.categoryBits = cat
        #self.body.maskBits = mask
        for fixture in self.body.fixtures:
            fixture.filterData.categoryBits = cat
            fixture.filterData.maskBits = mask
    def SetGraphicBody(self,body):
        self.body = body
        self.body.userData = self
        self.nx,self.ny = rr05(self.body.position)
    def CollisionCallBack(self):
        print "Collision detected"
    def SetBodyPosition(self,position):
        if self.body:
            self.body.position = position
    def SetBodyLinearVelocity(self,velocity):
        if self.body:
            self.body.linearVelocity = velocity
    def SetParent(self,parent):
        self.parent = parent
    def Draw(self,screen):
        pass
    def GetCode(self):
        return {"type":self.type,"drawMode":"ND"}
    def AddLastPos(self,pos,vel,instant):
        pass
        #self.last_positions[str(instant)] = {"pos":pos,"vel":vel,"ins":instant}
        #if self.last_positions.has_key(str(instant-300)):
        #    del self.last_positions[str(instant-300)]
    def Freeze(self):
        self.body.active = False
    def UnFreeze(self):
        self.body.active = True
    def SetLinear(self,vel):
        pass
    def Interpolate(self):
        #if not self.IntEnb:
        #    return
        #if self.body.active:
        #    return

        position = rr05(self.body.position)

        #nx = self.listGoTo[0][0]
        #ny = self.listGoTo[0][1]
        xd = self.nx - position[0]
        yd = self.ny - position[1]
        if xd < config.threshold:
            self.body.position[0] = self.nx
        else:
            self.body.position[0] += xd * config.interpolation_constant

        if yd < config.threshold:
            self.body.position[1] = self.ny
        else:
            self.body.position[1] += yd * config.interpolation_constant
    def SetPosition(self,position,lv=(0,0)):
        #print "New server position" , self.nx, self.ny
        #if self.body.active:
        #    self.body.position = position
        #    self.body.linearVelocity = lv
        #else:
        self.nx, self.ny = position
        #self.listGoTo.append(position)

class ImageElement(Element): #### ENVIABLE ####
    def __init__(self,handler,side = -1):
        Element.__init__(self,handler)
        self.type = "ImageElement"
        self.image = None
        self.codeMode = True
        self.side = side
    def DisableCodeMode(self):
        self.codeMode = False
    def SetImage(self,image):
        self.image = image
    def Draw(self,screen):
        if self.codeMode and self.image:
            if self.side == -1:
                image = Heads.codes[self.image]
            else:
                image = Heads.codes[self.image][self.side]
        screen.blit(image,(self.body.position[0]*self.handler.PPM - image.get_size()[0]/2,self.handler.pixelHeight-self.body.position[1]*self.handler.PPM - image.get_size()[1]/2))
    def GetCode(self):
        return {"type":self.type,"image":self.image,"position":rr05(self.body.position),"lv":rr05(self.body.linearVelocity),"side":self.side}

class DrawElement(Element): #### ENVIABLE ####
    def __init__(self,handler):
        Element.__init__(self,handler)
        self.type = "RectElement"
        self.color = 255,255,255
        self.draw = True
    def SetRect(self,color,position,size):
        body = self.handler.world.CreateStaticBody( position=( position[0],position[1]),shapes=polygonShape(box=(size[0], size[1])),color=(0,0,0) )
        self.SetGraphicBody(body)
        self.color = color
        self.size = size
    def SetColor(self,color):
        self.color = color
    def Draw(self,screen):
        if self.body and self.handler and self.draw:
            for fixture in self.body.fixtures:
                fixture.shape.draw(self.body, fixture , self.handler , self.color,screen)
    def SetDraw(self,draw):
        self.draw = draw
    def GetCode(self):
        return {"type":self.type,"position":rr05(self.body.position),"size":self.size,"color":self.color}

class Player(ImageElement): #### ENVIABLE ####
    def __init__(self , playerImage,handler,side):
        ImageElement.__init__(self,handler,side)
        self.type = "Player"
        self.SetImage(playerImage)
        body = handler.world.CreateDynamicBody()
        body.CreateCircleFixture(radius=1.3, density=400, friction=0)
        self.SetGraphicBody(body)
        self.jumpLast = time.time()
    def UpdateActions(self,actions):
        move_x = 0
        if actions.has_key("right"):
            move_x += 1
        if actions.has_key("left"):
            move_x -= 1
        self.Movement( move_x , actions.has_key("up"))
    def Movement(self,move,jump):
        if move == 1:
            v_line = 10
        elif move == -1:
            v_line = -10
        elif move == 0:
            v_line = 0
        if jump and self.body.position[1] < 2.5 and time.time() - self.jumpLast > 0.5:
            self.jumpLast = time.time()
            h_line = 15
        else:
            h_line = 0
        self.body.linearVelocity = v_line, self.body.linearVelocity[1]+h_line

class Ball(DrawElement):  #### ENVIABLE ####
    def __init__(self,handler,position,lv,color,rad=0.475):
        DrawElement.__init__(self,handler)
        self.type = "Ball"

        body = self.handler.world.CreateDynamicBody(bullet=True)
        body.position = position
        body.linearVelocity = lv
        self.circle = body.CreateCircleFixture(radius=rad, density=200, friction=0.1 ,restitution=0.95)
        self.SetColor(color)
        self.SetGraphicBody(body)

        self.radius = rad
        self.IntEnb = False
    def GetCode(self):
        return {"type":self.type,"color":self.color,"radius":self.radius,"position":rr05(self.body.position),"lv":rr05(self.body.linearVelocity)}
    def CollisionCallBack(self,player):
        self.handler.CollisionCallBack(self,player)

class ScoreSystemCont:
    def __init__(self):
        pass
    def AddWord(self,word,color,time,font="Classic",autoremoveTime=3):
        print "addd word"
        if self.target:
            self.target.HandleCentralWord(word,color,time,font)
        else:
            self.extraDraw["Animation"].AddWord(word,color,time,font,autoremoveTime)
    def EndLoop(self):
        return self.extraDraw["Animation"].EndLoop()
    def RemoveWord(self):
        if self.target:
            self.target.HandleRemoveCentralWord()
        else:
            self.extraDraw["Animation"].RemoveWord()

class ClockSystemCont:
    def __init__(self,duration):
        self.clock = ClockSystem(duration,self)
        self.extraDraw["clock"] = self.clock
    def UpdateClockSurface(self):
        self.clock.UpdateSurface()
    def UpdateClock(self):
        self.clock.LogicUpdate()
        if not self.target:
            self.UpdateClockSurface()
    def AddClock(self):
        self.clock.Enable()
        if self.target:
            self.target.HandleShowClock()
        else:
            self.clock.EnableGraphic()
    def RemoveClock(self):
        self.clock.Disable()
        if self.target:
            self.target.HandleRemoveClock()
        else:
            self.clock.DisableGraphic()
    def PlayClock(self):
        self.clock.Play()
        if self.target:
            self.target.HandlePlayClock()
    def StopClock(self,send=False,ins=-1):
        self.clock.Stop(instant=ins)
        if self.target and send:
            self.target.HandleStopClock(self.clock.time)

class PowerGameEngine(ScoreSystemCont,ClockSystemCont):
    def __init__(self,mode):

        self.elements = dict() #### LOS QUE SE MUEVEN MUCHO ####
        self.static = dict() #### LOS QUE ESTAN SEMI QUIETOS ####
        self.extraDraw = dict() #### CRONOMETRO , MARCADOR ####
        self.balls = []

        self.PPM = 20.0
        self.FPS = 40.0
        self.TIME_STEP = 1.0/ self.FPS
        self.contactListener = contactL.MyContactListener()
        self.world = Box2D.b2World(gravity=(0,-30),doSleep=True,contactListener=self.contactListener) #The Box2D world


        self.pixelHeight = 600
        self.pixelWidth = 900

        self.id = -1
        self.sid = -1

        self.background = 255,100,0
        self.mode = mode
        self.target = None
        self.clientTarget = None
        self.loopEnabled = True

        self.players = dict()

        self.gameStarted = False
        self.clockPlaying = False
        self.playsA = 0
        self.playsB = 0
        self.maxA = 1
        self.maxB = 1
        self.scoreA = None
        self.scoreB = None
        self.match_duration = config.match_duration #min
        self.time = 0
        self.refTimeStopStart = 0
        self.refTimeStart = 0
        self.clock = ClockSystem(self.match_duration,self)


        self.updateFrec = None
        self.clockUpdateFrec = 0.5
        self.refUpdate = time.time()*1000

        self.AteamName = None
        self.BteamName = None
        self.is_in_goal = False

        self.instant = 0
        self.showScore = False
        #self.SetMaxPlayers(1,1)
        #self.SetATeamName("Newtonis")
        #self.SetBTeamName("GranDT")
        #self.SetScoreA(5)
        #self.SetScoreB(0)
        self.numberSequence = -1
        self.my_player = -1

        self.centralText = None
        self.centralFont = None

        self.status = "playBall"
        self.half = "first"

        self.auto = False
        self.animationStatus = "noPlaying"
        self.worldVersion = 0
        self.do_step = True

        self.sideServer = 0
        self.lastGoal = -1

        self.move = True

        ClockSystemCont.__init__(self,self.match_duration)
    def GetServer(self):
        if self.lastGoal != -1:
            if self.lastGoal == 0:
                self.lastGoal = -1
                return 1
            elif self.lastGoal == 1:
                self.lastGoal = -1
                return 0
        else:
            if self.sideServer == 0:
                self.sideServer = 1
            else:
                self.sideServer = 0

        return self.sideServer
    def GetServerBallLV(self):
        if self.GetServer() == 0:
            return (-10,10)
        else:
            return (10,10)
    def SetAuto(self):
        self.auto = True
        #self.StartGame()
    def StartSequence(self):
        self.numberSequence = 3
        self.refSequence = time.time()*1000
        if self.target:
            self.target.HandleStartSequence()
    def UpdateSequence(self):
        if time.time()*1000-self.refSequence > 1000:
            self.refSequence = time.time() * 1000
            self.numberSequence -= 1
        if not self.target:
            if self.numberSequence > 0:
                self.UpdateSequenceSurface()
            else:
                self.DeleteExtraDraw("sequence")
    def UpdateSequenceSurface(self):
        surface = fonts.Absender.c80.render(str(self.numberSequence),1,(0,0,0))
        self.extraDraw["sequence"] = Surface(surface,(self.pixelWidth/2-surface.get_size()[0]/2,200))
    def StartGame(self):
        self.gameStarted = True
        if self.target:
            self.target.HandleStartGame()
        else:
            pass
    def GoNextHalf(self):
        self.SwitchSides()
        self.part = "ST"
    def SwitchSides(self):
        pass

    def GiveGoalA(self):
        self.lastGoal = 0
        self.SetScoreA(self.scoreA+1)
    def GiveGoalB(self):
        self.lastGoal = 1
        self.SetScoreB(self.scoreB+1)
    def SetScoreA(self,score):
        self.scoreA = score

        if not self.showScore:
            return

        if self.target:
            self.target.HandleNewScore("A",self.scoreA)
            if score != 0:
                self.StopClock()
        else:
            print "set score"
            self.extraDraw["Score"].SetScore("A",score)
            #if score != 0:
            #    self.animationGoal = "A"
            #    self.StopClock()
            #    self.StartGoalAnimation()
            #else:
            #    self.UpdateScoreASurface()
    def SetScoreB(self,score):
        self.scoreB = score
        if not self.showScore:
            return

        if self.target:
            self.target.HandleNewScore("B",self.scoreB)
            if score != 0:
                self.StopClock()
        else:
            print "set score"
            self.extraDraw["Score"].SetScore("B",score)
            #if score != 0:
            #    self.animationGoal = "B"
            #    self.StopClock()
            #    self.StartGoalAnimation()
            #else:
            #    self.UpdateScoreBSurface()
    def StartGoalAnimation(self):
        self.goalAnimation = True

        y_pos = 200
        duration = 20

        width = BoomBox("A").get_size()[0]
        self.extraDraw["GOAL"] = LettersAnimation("GOAL",(100,100,200),self)
        #self.extraDraw["G"] = AnimationLetter("G",(self.pixelWidth/2-150-width/2,y_pos),(-100,-100),duration)
        #self.extraDraw["O"] = AnimationLetter("O",(self.pixelWidth/2-50-width/2,y_pos),(-100,self.pixelHeight),duration)
        #self.extraDraw["A"] = AnimationLetter("A",(self.pixelWidth/2+50-width/2,y_pos),(self.pixelWidth,-100),duration)
        #self.extraDraw["L"] = AnimationLetter("L",(self.pixelWidth/2+150-width/2,y_pos),(self.pixelWidth,self.pixelHeight),duration)
        self.animationStatus = "playing"
    def UpdateScoreASurface(self,y=20):
        text = fonts.BebasNeue.c60.render(str(self.scoreA),1,(0,0,0))
        self.extraDraw["scoreA"] = Surface(text,(self.pixelWidth/2-30-text.get_size()[0],y))
        if not self.extraDraw.has_key("-"):
            text = fonts.BebasNeue.c60.render("-",0,(0,0,0))
            self.extraDraw["-"] = Surface(text,(self.pixelWidth/2-9,20))
    def UpdateScoreBSurface(self,y=20):
        text = fonts.BebasNeue.c60.render(str(self.scoreB),1,(0,0,0))
        self.extraDraw["scoreB"] = Surface(text,(self.pixelWidth/2+30,y))
        if not self.extraDraw.has_key("-"):
            text = fonts.BebasNeue.c60.render("-",0,(0,0,0))
            self.extraDraw["-"] = Surface(text,(self.pixelWidth/2-9,20))
    def DeleteScore(self):
        self.showScore = False
        if self.target:
            self.target.HandleScoreDeleted()
        else:
            self.extraDraw["Score"].Disable()
    def AddScore(self):
        self.showScore = True
        self.scoreA = 0
        self.scoreB = 0
        #self.SetScoreA(0)
        #self.SetScoreB(0)
        if self.target:
            self.target.HandleScoreAdded()
        else:
            self.extraDraw["Score"].Enable()
    def SetATeamName(self,name):
        self.AteamName = name
        if self.target:
            self.target.TeamANameSet(name)
        else:
            self.GenerateAteamSurface()
    def SetBTeamName(self,name):
        self.BteamName = name
        if self.target:
            self.target.TeamBNameSet(name)
        else:
            self.GenerateBteamSurface()
    def RemoveTeamAName(self):
        self.AteamName = None
        if self.target:
            self.target.TeamANameOut()
        else:
            del self.extraDraw["teamA"]
    def RemoveTeamBName(self):
        self.BteamName = None
        if self.target:
            self.target.TeamBNameOut()
        else:
            del self.extraDraw["teamB"]
    def RemoveBothNames(self):
        if self.target:
            self.target.NamesRemoved()
        else:
            if self.extraDraw.has_key("teamA"):
                del self.extraDraw["teamA"]
            if self.extraDraw.has_key("teamB"):
                del self.extraDraw["teamB"]
    def GenerateAteamSurface(self):
        text = fonts.BebasNeue.c40.render(self.AteamName,1,(0,0,0))
        self.extraDraw["teamA"] = Surface(text,(self.pixelWidth/2-200-text.get_size()[0],30))
    def GenerateBteamSurface(self):
        text = fonts.BebasNeue.c40.render(self.BteamName,1,(0,0,0))
        self.extraDraw["teamB"] = Surface(text,(self.pixelWidth/2+200,30))
    def SetMaxPlayers(self,maxA,maxB):
        self.maxA = maxA
        self.maxB = maxB
        self.maxEnabled = True
        if self.target:
            self.target.HandlerMaxPlayers(maxA,maxB)
        else:
            self.UpdateMaxSurfaces()
    def DisableMaxPlayers(self):
        self.maxEnabled = False
        if self.target:
            self.target.HandleDisableMax()
        else:
            self.DeleteExtraDraw("maxA")
            self.DeleteExtraDraw("maxB")
    def MaxData(self):
        return {"enb":self.maxEnabled,"maxA":self.maxA,"maxB":self.maxB,"ca":self.playsA,"cb":self.playsB}
    def HandleMaxCode(self,maxData):
        if maxData["enb"]:
            self.playsA = maxData["ca"]
            self.playsB = maxData["cb"]
            self.SetMaxPlayers(maxData["maxA"],maxData["maxB"])
    def UpdateMaxSurfaces(self):
        maxA = fonts.BebasNeue.c50.render(str(self.playsA)+"/"+str(self.maxA),1,(100,100,100))
        maxB = fonts.BebasNeue.c50.render(str(self.playsB)+"/"+str(self.maxB),1,(100,100,100))

        self.extraDraw["maxA"] = Surface(maxA,(self.pixelWidth/8-maxA.get_size()[0]/2,self.pixelHeight-250))
        self.extraDraw["maxB"] = Surface(maxB,(self.pixelWidth/8*7-maxB.get_size()[0]/2,self.pixelHeight-250))
    def UpdatePlaysA(self,playsA):
        self.playsA = playsA
        if self.target:
            self.target.HandleChangePlays('A',playsA)
        else:
            self.UpdateMaxSurfaces()
    def UpdatePlaysB(self,playsB):
        self.playsB = playsB
        if self.target:
            self.target.HandleChangePlays('B',playsB)
        else:
            self.UpdateMaxSurfaces()
    def DeleteExtraDraw(self,id):
        if self.extraDraw.has_key(id):
            del self.extraDraw[id]
    def SetTarget(self,target):
        self.target = target
    def SetClientTarget(self,target):
        self.clientTarget = target
        self.extraDraw["Animation"] = LetterSystem(self)
        self.extraDraw["Score"] = ScoreSystem(self)
        self.extraDraw["Score"].SetLetterSystem(self.extraDraw["Animation"])
        #self.AddWord("Test MSJ",(100,100,200),20)
    def AddPlayer(self,headCode,playerName,id=-1):
        if playerName == "A1":
            position = (4,3)
            side = 0

        elif playerName == "A2":
            position = (41,3)
            side = 1

        player = Player(headCode,self,side)
        if side == 0:
            player.SetMask(LAYER_1,LAYER_1 | LAYER_2 | LAYER_3 | LAYER_4)
        elif side == 1:
            player.SetMask(LAYER_2,LAYER_1 | LAYER_2 | LAYER_3 | LAYER_4)
        #player.Freeze()


        #player.()
        player.SetBodyPosition(position)
        final_id = self.AddElement(player,id)
        self.players[playerName] = final_id
        return final_id
    def ResetPlayersPositions(self):
        if self.players.has_key("A1"):
            self.elements[self.players["A1"]].body.position = (4,3)
        if self.players.has_key("A2"):
            self.elements[self.players["A2"]].body.position = (41,3)
    def AddBall(self,lv="default",position=(22.5,20),color=(100,100,100),id=-1):
        self.is_in_goal = False
        if lv == "default":
            lv = self.GetServerBallLV()
        ball = Ball(self,position,lv,color)
        ball.SetMask(LAYER_4 , LAYER_1 | LAYER_2 | LAYER_3 | LAYER_4)
        id = self.AddElement(ball,id)
        self.balls.append(id)
        return id
    def AddElement(self,element,id=-1):
        if id == -1:
            id = self.NextID()
        self.elements[str(id)] = element
        self.elements[str(id)].id = str(id)
        if self.target:
            self.target.DynamicElementAdded(element.GetCode(),id)
        return str(id)
    def DeleteElement(self,id):
        if not self.elements.has_key(id):
            return
        self.world.DestroyBody(self.elements[id].body)
        for x in range(len(self.balls)):
            if self.elements[self.balls[x]] == self.elements[id]:
                del self.balls[x]
                break
        del self.elements[id]

        if self.target:
            self.target.DynamicElementDeleted(id)
    def UpdateDynamicElement(self,id,position,lv):
        self.elements[str(id)].body.position = position
        self.elements[str(id)].body.linearVelocity = lv
    def AddStaticElement(self,element,id = -1):
        if id == -1:
            id = self.NextStaticID()
        self.static[str(id)] = element
    def DeleteStaticElement(self,id):
        del self.static[str(id)]
    def CreateElements(self,data):
        for element in data:
            self.CreateElement(element)
    def CreateElement(self,element):
        if element["type"] == "ImageElement":
            new_element = ImageElement(self)
            new_element.SetImage(element["image"])
            new_element.SetBodyPosition(element["position"])
            new_element.SetBodyLinearVelocity(element["lv"])
            self.AddElement(new_element,element["id"])
        elif element["type"] == "Ball":
            new_element = Ball(self,element["position"],element["lv"],element["color"],element["radius"])
            new_element.SetMask( LAYER_3 , LAYER_1 | LAYER_2 | LAYER_3)
            #new_element.Freeze()
            id = self.AddElement(new_element,element["id"])
            self.balls.append(id)
        elif element["type"] == "Player":
            new_element = Player(element["image"],self,element["side"])
            new_element.SetBodyPosition(element["position"])
            new_element.SetBodyLinearVelocity(element["lv"])
            new_element.Freeze()
            if element["side"] == 0:
                print "side A-------"
                new_element.SetMask(LAYER_1, LAYER_1 | LAYER_3)
            elif element["side"] == 1:
                print "side B-------"
                new_element.SetMask(LAYER_2, LAYER_2 | LAYER_3)
            self.AddElement(new_element,element["id"])
    def AddRectStaticElement(self,draw,position,size,color):
        new_element = DrawElement(self)
        new_element.SetDraw(draw)
        new_element.SetRect(color,position,size)
        new_element.SetMask(LAYER_3,LAYER_1 | LAYER_2 | LAYER_3 | LAYER_4)
        self.AddStaticElement(new_element)
    def AddPitchStatics(self):
        self.AddRectStaticElement(False,(1.5,8.25) ,(1.4, 0.2),(0,0,0))
        self.AddRectStaticElement(False,(0.0, 0.0) ,(0.5,30.0),(0,0,0))
        self.AddRectStaticElement(False,(43.5,8.25),(1.5, 0.2),(0,0,0))
        self.AddRectStaticElement(False,(44.8,   0),(0.2,30.0),(0,0,0))
        self.AddRectStaticElement(True,(   0,   0),( 50,   1),(0,100,0))
        self.AddRectStaticElement(False,(   0,29.9),( 50, 0.1),(0,0,0))
    def AddPitch(self,pitchname = "classic"):
        self.pitch_type = pitchname
        if pitchname == "classic":
            self.AddPitchStatics()
            self.SetBackground((200,200,255))
            self.AddGoals(Heads.goalClassic)

    def AddGoals(self,animation):
        self.AddGoalA(animation)
        self.AddGoalB(animation)
    def AddGoalA(self,animation):
        self.AddGoal((0,self.pixelHeight-170),"GoalA",0,animation)
    def AddGoalB(self,animation):
        self.AddGoal((self.pixelWidth-60,self.pixelHeight-170),"GoalB",1,animation)
    def AddGoal(self,position,name,side,animation):
        self.extraDraw[name] = Animation(animation,position,side)
    def GoalEffect(self,goal):
        self.extraDraw[goal].StartAnimation()
    def ResetGoalEffects(self):
        self.extraDraw["GoalA"].Reset()
        self.extraDraw["GoalB"].Reset()
    def HandlePlayerActions(self,playerID,actions):
        if self.move:
            self.elements[ self.players[str(playerID)] ].UpdateActions(actions)
    def SetBackground(self,background):
        self.background = background
    def InitialContent(self,data):
        self.background = data["background"]
        self.CreateElements(data["elements"])
    def UpdateElementPosition(self,id,position,lv):
        if self.elements.has_key(str(id)):
            self.elements[str(id)].SetPosition(position,lv)
            #self.elements[str(id)].SetLinear(lv)
    def NextID(self):
        self.id += 1
        return self.id
    def NextStaticID(self):
        self.sid += 1
        return self.sid
    def Loop(self):
        lp = dict()

        #if self.target:
        if self.do_step:
            self.world.Step(self.TIME_STEP,10,10)


        if self.target and self.updateFrec:
            period = 1.0/self.updateFrec
            if time.time()*1000-self.refUpdate > period * 1000:
                self.refUpdate = time.time()*1000
                #for ball in self.balls:
                #    self.target.HandleElementMove(-1,ball,rr05(self.elements[ball].body.position),rr05(self.elements[ball].body.linearVelocity),True)

                self.target.HandleUpdateMovement()
    def LogicUpdate(self):
        for dd in self.extraDraw.keys():
            self.extraDraw[dd].LogicUpdate()
        if not self.target:
            for element in self.elements.keys():
                self.elements[element].Interpolate()
        if self.loopEnabled:
            self.instant += 1
            self.Loop()

        if self.extraDraw.has_key("GoalA") and self.extraDraw.has_key("GoalB"):
            results = self.SomethingGoal()
            for result in results:
                if self.target:
                    if not self.is_in_goal:
                        self.elements[result["element"]].body.linearVelocity[0] = self.elements[result["element"]].body.linearVelocity[0] / 4
                        self.elements[result["element"]].body.linearVelocity[1] = self.elements[result["element"]].body.linearVelocity[1] / 4
                        self.target.HandleGoalScored(result["goal"])
                        self.is_in_goal = True
                else:
                    if not self.is_in_goal:
                        self.elements[result["element"]].body.linearVelocity[0] = self.elements[result["element"]].body.linearVelocity[0] / 4
                        self.elements[result["element"]].body.linearVelocity[1] = self.elements[result["element"]].body.linearVelocity[1] / 4
                        self.is_in_goal = True

                    self.GoalEffect(result["goal"])

        if self.numberSequence != -1:
            self.UpdateSequence()
        if self.gameStarted:
            self.UpdateClock()
        self.UpdateScoreAnimation()
    def UpdateScoreAnimation(self):
        if self.animationStatus == "playing":
            if self.extraDraw["GOAL"].EndLoop(): ### HALF ANIMATION ###
                self.animationStatus = "scoreAnimation"
        elif self.animationStatus == "scoreAnimation":
            if self.animationGoal == "A":
                current = "scoreA"
            elif self.animationGoal == "B":
                current = "scoreB"
            if self.extraDraw[current].y > -100:
                self.extraDraw[current].y -= 3
            else:
                self.animationStatus = "changeWait"

        elif self.animationStatus == "changeWait":
            if self.animationGoal == "A":
                self.UpdateScoreASurface(self.extraDraw["scoreA"].y)
            elif self.animationGoal == "B":
                self.UpdateScoreBSurface(self.extraDraw["scoreB"].y)
            self.animationStatus = "scoreAnimationB"
        elif self.animationStatus == "scoreAnimationB":
            if self.animationGoal == "A":
                current = "scoreA"
            elif self.animationGoal == "B":
                current = "scoreB"
            if self.extraDraw[current].y < 20:
                self.extraDraw[current].y += 3
            else:
                self.animationStatus = "go2backplaying"
        elif self.animationStatus == "go2backplaying":
            self.extraDraw["GOAL"].Reverse()
            self.animationStatus = "EndDone"
        elif self.animationStatus == "EndDone":
            pass
    def UnclockGoals(self):
        self.extraDraw["GoalA"].Unclock()
        self.extraDraw["GoalB"].Unclock()
    def GraphicUpdate(self,screen):
        screen.fill(self.background)
        for sk in self.static.keys():
            self.static[sk].Draw(screen)
        for dd in self.extraDraw.keys():
            self.extraDraw[dd].GraphicUpdate(screen)
        for ek in self.elements.keys():
            self.elements[ek].Draw(screen)
    def SomethingGoal(self):
        result = []
        for ball in self.balls:
            if self.elements[ball].body.position[0] < 3 and self.elements[ball].body.position[1] < 7.5:
                result.append({"element":ball,"goal":"GoalA"})
            elif self.elements[ball].body.position[0] > 42 and self.elements[ball].body.position[1] < 7.1:
                result.append({"element":ball,"goal":"GoalB"})
            if self.elements[ball].body.position[0] > 4 and self.elements[ball].body.position[0] < 41:
                self.UnclockGoals()
        return result
    def GetDynamicCodes(self):
        codes = []
        for key in self.elements.keys():
            element = self.elements[key].GetCode()
            element["id"] = key
            codes.append(element)
        return codes
    def CollisionCallBack(self,ball,player): ### IN CLIENT MODE WHEN YOUR PLAYER HITS THE BALL IN CURRENT WORLD
        #print player.name
        if self.clientTarget and player.id == self.my_player:
            self.clientTarget.PlayerCollision(player.body.position,player.body.linearVelocity,ball.body.position,ball.body.linearVelocity)
    def SetPlayer(self,player_id):
        self.my_player = player_id
    def AddCentralText(self,text,font,y=150):
        return
        self.centralText = text
        self.centralFont = font
        if self.target:
            self.target.HandleAddText(text,font,y)
        else:
            if font == "Bebas20":
                font = fonts.BebasNeue.c20
            elif font == "Bebas30":
                font = fonts.BebasNeue.c30
            elif font == "Bebas40":
                font = fonts.BebasNeue.c40
            surface = font.render(text,1,(0,0,0))
            sw,sh = surface.get_size()
            self.extraDraw["central-text"] = Surface(surface,(self.pixelWidth/2-sw/2,y))
    def DeleteCentralText(self):
        self.centralText = None
        self.centralFont = None
        if self.target:
            self.target.HandleRemoveText()
        else:
            self.DeleteExtraDraw("central-text")
    def GetCentralData(self):
        if self.centralText:
            return {"text":self.centralText,"font":self.centralFont}
        else:
            return None
    def EndTime(self):
        if self.half == "halftime":
            return True

        return False
    def GetData(self):
        data = dict()
        data["pitch_name"] = self.pitch_type
        data["pitch_content"] = self.GetDynamicCodes()
        data["max_data"] = self.MaxData()
        data["nameA"] = self.AteamName
        data["nameB"] = self.BteamName
        data["scoreA"] = self.scoreA
        data["scoreB"] = self.scoreB
        data["central-text"] = self.GetCentralData()
        data["server"] = self.sideServer
        return data
    def SetData(self,data):
        if data.has_key("pitch_name"):
            self.AddPitch(data["pitch_name"])
        if data.has_key("pitch_content"):
            self.CreateElements(data["pitch_content"])
        if data.has_key("max_data"):
            self.HandleMaxCode(data["max_data"])
        if data.has_key("nameA"):
            if data["nameA"]:
                self.SetATeamName(data["nameA"])
        if data.has_key("nameB"):
            if data["nameB"]:
                self.SetBTeamName(data["nameB"])
        if data.has_key("scoreA"):
            if data["scoreA"]:
                self.SetScoreA("scoreA")
        if data.has_key("scoreB"):
            if data["scoreB"]:
                self.SetScoreB("scoreB")
        if data.has_key("central-text"):
            if data["central-text"]:
                info = data["central-text"]
                text = info["text"]
                font = info["font"]
                self.AddCentralText(text,font)
        if data.has_key("server"):
            self.sideServer = data["server"]
    def EnableMove(self):
        self.move = True
    def DisableMove(self):
        self.move = False
    def GetWinner(self):
        if self.scoreA > self.scoreB:
            return "A"
        elif self.scoreA < self.scoreB:
            return "B"
        else:
            return "ND"
    def GetWinnerText(self):
        win = self.GetWinner()
        if win == "A":
            return str(self.AteamName) + " wins the match"
        elif win == "B":
            return str(self.BteamName) + " wins the match"
        else:
            return "It's a draw"

def get_key_actions(keys):
    values = dict()
    if keys[pygame.K_UP]:
        values["up"] = True
    if keys[pygame.K_LEFT]:
        values["left"] = True
    if keys[pygame.K_RIGHT]:
        values["right"] = True
    return values