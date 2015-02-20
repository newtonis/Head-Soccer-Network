__author__ = 'newtonis'

import pygame
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.ServerUDP import ServerUDP
from Box2D.b2 import *

from source.data.images import *

def my_draw_polygon(polygon, body, fixture , handler ,color ,screen):
    vertices=[(body.transform*v)*handler.PPM for v in polygon.vertices]
    vertices=[(v[0], handler.pixelHeight-v[1]) for v in vertices]
    pygame.draw.polygon(screen, color, vertices)
polygonShape.draw=my_draw_polygon

def my_draw_circle(circle, body, fixture , handler ,color ,screen):
    position=body.transform*circle.pos*handler.PPM
    position=(position[0], handler.pixelHeight-position[1])
    pygame.draw.circle(screen, color, [int(x) for x in position], int(circle.radius*handler.PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.
circleShape.draw=my_draw_circle

class Element:
    def __init__(self,handler,body,position,linearVelocity,drawMode,color=None,image=None,side = -1):
        self.body     = body
        self.body.position       = position
        self.body.linearVelocity = linearVelocity
        self.color    = color
        self.drawMode = drawMode #if it is an image or a figure like a circle or a square
        self.image    = image
        self.handler  = handler
        self.type = "Element"
        self.side = side
        self.xpos,self.ypos = 0,0
    def SetType(self,type):
        self.type = type
    def SetPosition(self,position):
        self.body.position = position
    def GetPosition(self):
        return self.body.position[0] , self.body.position[1]
    def SetLinearVelocity(self,velocity):
        self.body.linearVelocity = velocity
    def GetLinearVelocity(self):
        return self.body.linearVelocity[0] , self.body.linearVelocity[1]
    def ResetLinearVelocity(self):
        self.SetLinearVelocity((0,0))
    def Draw(self,screen,rects = []):

        if self.drawMode == "polygon":
            for fixture in self.body.fixtures:
                fixture.shape.draw(self.body, fixture , self.handler , self.color,screen)
        elif self.drawMode == "image":
            if self.side == -1:
                image = Heads.codes[self.image]
            else:
                image = Heads.codes[self.image][self.side]
            lxpos,lypos = self.xpos,self.ypos
            self.xpos,self.ypos = (self.body.position[0]*self.handler.PPM - 30,(screen.get_size()[1]-self.body.position[1]*self.handler.PPM)  -30 )
            screen.blit(image , (self.xpos,self.ypos) )
            #w,h = image.get_size()

            #rects.append([int(lxpos),int(lypos),w,h])
            #rects.append([ int(self.xpos),int(self.ypos),w,h])

        #return rects
    def GetCode(self):
        return {"type":self.type,"position":self.GetPosition(),"velocity":self.GetLinearVelocity(),"drawMode":self.drawMode,"image":self.image}

class ShowImage:
    def __init__(self,image,position,mode = "normal"):
        self.image    = image
        self.position = position
        self.mode     = mode
    def Draw(self , screen,rects = None):
        if self.mode == "normal":
            screen.blit(Heads.codes[self.image],self.position)
            w,h = Heads.codes[self.image].get_size()
            #if rects:
            #    rects.append( [self.position[0],self.position[1],w,h] )

class Player:
    def __init__(self,element):
        self.element = element
    def UpdateActions(self,actions):
        move_x = 0
        if actions["right"]:
            move_x += 1
        if actions["left"]:
            move_x -= 1
        self.Movement( move_x , actions["up"])
    def Movement(self , move , jump):
        if move == 1:
            v_line = 10
            #self.body.linearVelocity=(90,16.445)
        elif move == -1:
            v_line = -10
            #self.body.linearVelocity=(90,16.445)
        elif move == 0:
            v_line = 0

        if jump == True and self.element.GetPosition()[1] < 2.5:
            h_line = 15
        else:
            h_line = 0
        #if self.enabled:
        #    SpeedBotin = 5
        #else:
        #    SpeedBotin = 0
        self.element.SetLinearVelocity((v_line, self.element.GetLinearVelocity()[1]+h_line))



#GAME ENGINE FOR A BASIC PLAYROOM
class GameSys:
    def __init__(self):
        self.PPM       = 20.0
        self.FPS       = 40.0
        self.TIME_STEP = 1.0 / self.FPS
        self.world     = world(gravity=(0,-30),doSleep=True) #The Box2D world
        self.elements  = dict()
        self.ballID    = None
        self.playerAID = None #The ID of the player A element
        self.playerBID = None #The ID of the player B element
        self.pitchIDs  = []   #The IDs of the pitch elements

        self.playerA   = None #The ID of the playe A manager
        self.playerB   = None #The ID of the playe B manager

        self.ballColor  = 200,200,200
        self.background  = 0,0,0
        self.playerAHead = "Head A" #head code
        self.playerBHead = "Head B" #head code

        self.Log = [] #register of what happened
        self.width = 45
        self.height = 30
        self.CalculateHalfs()

        self.idCount     = 0
        self.showThings  = dict()
        self.idShowCount = 0

        self.counterGoalA = 0 #Used for the goal scored animation
        self.counterGoalB = 0

        self.targetAction = None #Who will handle the goals
        self.stadium = None
        self.first = True

        self.target = None
        self.AddLog("Starting game ...")
    def SetTarget(self,target):
        self.target = target
    def NextId(self):
        self.idCount += 1
        return self.idCount
    def NextCountId(self):
        self.idShowCount += 1
        return self.idShowCount
    def AddLog(self,msg):
        self.Log.append(msg)
    def SetStadium(self,stadium):
        self.AddLog("Traveling stadium '"+str(stadium)+"'")
        self.stadium = stadium
    def SetBackground(self,color):
        self.AddLog("Setting background color: "+str(color))
        self.background = color
    def SetTargetAction(self,target):
        self.targetAction = target
    def CalculateHalfs(self):
        self.HalfWidth   = self.width / 2
        self.HalfHeight  = self.height / 2
        self.pixelHalfWidth  = self.HalfWidth * self.PPM
        self.pixelHalfHeight = self.HalfHeight * self.PPM
        self.pixelWidth  = self.width * self.PPM
        self.pixelHeight = self.height* self.PPM
    def AddElement(self,element,id):
        self.AddLog("Element added with id "+str(id))
        self.elements[id] = element
        if self.target:
            self.target.ElementAdded(element,id)
    def RemoveElement(self,id):
        self.AddLog("Element removed with id "+str(id))
        self.world.DestroyBody(self.elements[id].body)
        del self.elements[id]
        if self.target:
            self.target.ElementDeleted(id)
    def ChangeElementPosition(self,id,position):
        self.elements[id].SetPosition(position)
    def ChangeElementLinearVelocity(self,id,velocity):
        self.elements[id].SetLinearVelocity(velocity)
    def GetElementPosition(self,id):
        return self.elements[id].GetPosition()
    def GetElementLinearVelocity(self,id):
        return self.elements[id].GetLinearVelocity()
    def DivideElementLinearVelocity(self,id,factor):
        self.ChangeElementLinearVelocity(id , (self.GetElementLinearVelocity(id)[0]/factor , self.GetElementLinearVelocity(id)[0]/factor) )
    def AddShowThing(self,id,image,position,mode="normal"):
        self.AddLog("Adding show thing with id "+str(id))
        self.showThings[id] = ShowImage(image,position,mode)
    def DeleteShowThing(self,id):
        self.AddLog("Deleting show thing "+str(id))
        del self.showThings[id]
    def ChangeShowThingImage(self,id,image):
        self.showThings[id].image = image
    def ChangeShowThingPosition(self,id,position):
        self.showThings[id].position = position
    def AddBall(self , position = None,lv = (0,10)):
        if not position:
            position = self.HalfWidth,self.HalfHeight
        if not self.ballID:
            self.AddLog("Adding ball ...")
        else:
            self.AddLog("Game has already a ball")
            return
        body         = self.world.CreateDynamicBody(bullet=True)

        circle       = body.CreateCircleFixture(radius=0.475, density=200, friction=0.1 ,restitution=0.95)
        element      = Element(self,body,position,lv,"polygon",self.ballColor)
        element.type = "Ball"
        #(self,handler,body,position,linearVelocity,drawMode,color=None,image=None)
        self.ballID  = self.NextId()
        self.AddElement(element,self.ballID)
    def RemoveBall(self):
        self.AddLog("Removing ball ...")
        self.RemoveElement(self.ballID)
        self.ballID = None
    def AddPlayerA(self,headCode , position = (3,8) , lv = (0,0) ):
        self.AddLog("Adding player A ...")
        self.playerAHead = headCode
        body = self.world.CreateDynamicBody()
        head = body.CreateCircleFixture(radius=1.3, density=400, friction=0)
        element = Element(self,body,position,lv,"image",None,self.playerAHead,0)
        element.SetType("PlayerA")
        self.playerAID = self.NextId()
        self.AddElement(element,self.playerAID)
        self.playerA = Player(element)
    def AddPlayerB(self,headCode , position = (42,8) , lv = (0,0)):
        self.AddLog("Adding player B ...")
        self.playerBHead = headCode
        body = self.world.CreateDynamicBody()
        head = body.CreateCircleFixture(radius=1.3,density=400,friction=0)
        element = Element(self,body,position,lv,"image",None,self.playerBHead,1)
        element.SetType("PlayerB")
        self.playerBID = self.NextId()
        self.AddElement(element,self.playerBID)
        self.playerB = Player(element)
    def RemovePlayerA(self):
        self.AddLog("Removing player A ...")
        self.RemoveElement(self.playerAID)
        self.playerAID = None
        self.playerB   = None
    def RemovePlayerB(self):
        self.AddLog("Removing player B ...")
        self.RemoveElement(self.playerBID)
        self.playerBID = None
        self.playerA   = None
    def ResetPlayersPositions(self):
        self.elements[self.playerAID].SetPosition((3,3))
        self.elements[self.playerBID].SetPosition((30,3))
        self.elements[self.playerAID].ResetLinearVelocity()
        self.elements[self.playerBID].ResetLinearVelocity()
    def AddPitch(self,background,stadium=None):
        self.background = background
        self.stadium = stadium
        self.AddLog("Adding pitch ...")
        #Creating Box2D elements
        bodyA = self.world.CreateStaticBody( position=( 1.5,8.25),shapes=polygonShape(box=(1.4, 0.2)),color=(0,0,0) )
        bodyB = self.world.CreateStaticBody( position=( 0.0, 0.0),shapes=polygonShape(box=(0.5,30.0)),color=(0,0,0) )
        bodyC = self.world.CreateStaticBody( position=(43.5,8.25),shapes=polygonShape(box=(1.5, 0.2)),color=(0,0,0) )
        bodyD = self.world.CreateStaticBody( position=(44.8,   0),shapes=polygonShape(box=(0.2,30.0)),color=(0,0,0) )
        bodyE = self.world.CreateStaticBody( position=(   0,   0),shapes=polygonShape(box=( 50,   1)),color=(0,0,0) )
        bodyF = self.world.CreateStaticBody( position=(   0,29.9),shapes=polygonShape(box=( 50, 0.1)),color=(0,0,0) )
        #Creating Common elements
        blueColor = 100,100,200
        elementA = Element(self,bodyA,( 1.5,8.25),(0,0),"invisible",(0,0,0))
        elementB = Element(self,bodyB,(   0,   0),(0,0),"invisible",(0,0,0))
        elementC = Element(self,bodyC,(43.5,8.25),(0,0),"invisible",(0,0,0))
        elementD = Element(self,bodyD,(44.8,   0),(0,0),"invisible",(0,0,0))
        elementE = Element(self,bodyE,(   0,   0),(0,0),"polygon",blueColor)
        elementF = Element(self,bodyF,(   0,29.9),(0,0),"invisible",(0,0,0))
        #Setting IDs
        idA = self.NextId()
        idB = self.NextId()
        idC = self.NextId()
        idD = self.NextId()
        idE = self.NextId()
        idF = self.NextId()
        #Adding elements
        self.AddElement(elementA,idA)
        self.AddElement(elementB,idB)
        self.AddElement(elementC,idC)
        self.AddElement(elementD,idD)
        self.AddElement(elementE,idE)
        self.AddElement(elementF,idF)
        #Saving IDs
        self.pitchIDs.append(idA)
        self.pitchIDs.append(idB)
        self.pitchIDs.append(idC)
        self.pitchIDs.append(idD)
        self.pitchIDs.append(idE)
        self.pitchIDs.append(idF)
        #Adding images
        self.idGoalA = self.NextCountId()
        self.idGoalB = self.NextCountId()
        self.AddShowThing(self.idGoalA,"goal",(0,self.pixelHeight-170))
        self.AddShowThing(self.idGoalB,"rgoal",(self.pixelWidth-60,self.pixelHeight-170))
    def AddElementWithCode(self,code):
        id = code["id"]
        element = Element(self,)
    def GoalEffectA(self):
        self.ChangeShowThingImage(self.idGoalA,"goalB")
    def GoalEffectB(self):
        self.ChangeShowThingImage(self.idGoalB,"rgoalB")
    def SetActions(self,actions,player):
        if player == "Player A":
            if self.playerA:
                self.playerA.UpdateActions(actions)
        elif player == "Player B":
            if self.playerB:
                self.playerB.UpdateActions(actions)
    def Loop(self):
        self.world.Step(self.TIME_STEP, 10, 10)
        self.UpdateGoals()
    def Draw(self,screen,rects=[]):
        screen.fill(self.background)
        if not self.stadium:
            screen.fill(self.background)
        else:
            pass
            #screen.blit(Heads.codes[self.stadium["code"]],(0,0))
        for ELK in self.elements.keys():
            EL = self.elements[ELK]
            #nrects =
            EL.Draw(screen,rects)
            #if nrects:
            #    rects = nrects
        for EDK in self.showThings.keys():
            ED = self.showThings[EDK]
            #nrects =
            ED.Draw(screen,rects)
            #if nrects:
            #    rects = nrects

        #if self.first:
        #    w,h = pygame.display.get_surface().get_size()
        #    self.first = False
        #    rects.append([0,0,w,h])
        #return rects
    def UpdateGoals(self):
        if self.ballID == None:
            return
        if self.GetElementPosition(self.ballID)[0] < 3 and self.GetElementPosition(self.ballID)[1] < 7.5:
            if self.counterGoalA == 0:
                self.showThings[self.idGoalA].image = "goalB"
                self.DivideElementLinearVelocity(self.ballID,4)
            self.counterGoalA = 40
            if self.targetAction != None:
                self.targetAction.ScoreA()

        if self.GetElementPosition(self.ballID)[0] > 42 and self.GetElementPosition(self.ballID)[1] < 7.5:
            if self.counterGoalB == 0:
                self.showThings[self.idGoalB].image = "rgoalB"
                self.DivideElementLinearVelocity(self.ballID,4)
            self.counterGoalB = 40
            if self.targetAction != None:
                self.targetAction.ScoreB()
        if self.counterGoalA > 0:
            self.counterGoalA -= 1
        else:
             self.showThings[self.idGoalA].image = "goal"
        if self.counterGoalB > 0:
            self.counterGoalB -= 1
        else:
            self.showThings[self.idGoalB].image = "rgoal"
    def PrintLog(self):
        for x in range(len(self.Log)):
            print "Log "+str(x)+" "+self.Log[x]
    def GetCodes(self):
        kk = []
        for ekey in self.elements.keys():
            element = self.elements[ekey]
            kk.append(element.GetCode())
        result = dict()
        result["dynamic_data"] = kk
        result["background"] = self.background
        result["stadium"] = self.stadium
        return result
    def GetShowThingsCodes(self):
        pass

def get_key_actions(keys):
    return {"up":keys[pygame.K_UP],"down":keys[pygame.K_DOWN],"left":keys[pygame.K_LEFT],"right":keys[pygame.K_RIGHT]}
def get_alternative_key_actions(keys):
    return {"up":keys[pygame.K_w],"down":keys[pygame.K_s],"left":keys[pygame.K_a],"right":keys[pygame.K_d]}

