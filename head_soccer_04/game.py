#!/usr/bin/env python

__author__ = 'ariel'
from pygame.locals import *

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from PodSixNet.ServerUDP import ServerUDP
from Box2D.b2 import *

from images.heads import *
import fonts
import time

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
    def __init__(self,handler,body,position,linearVelocity,drawMode,color=None,image=None):
        self.body     = body
        self.body.position       = position
        self.body.linearVelocity = linearVelocity
        self.color    = color
        self.drawMode = drawMode #if it is an image or a figure like a circle or a square
        self.image    = image
        self.handler  = handler
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
    def Draw(self,screen):
        if self.drawMode == "polygon":
            for fixture in self.body.fixtures:
                fixture.shape.draw(self.body, fixture , self.handler , self.color,screen)
        elif self.drawMode == "image":
            screen.blit(self.image , (self.body.position[0]*self.handler.PPM - (1.3)*self.handler.PPM,(screen.get_size()[1]-self.body.position[1]*self.handler.PPM)  -(1.3)*self.handler.PPM ) )

class ShowImage:
    def __init__(self,handler,image,position,mode = "normal"):
        self.image    = image
        self.position = position
        self.mode     = mode
        self.handler  = handler
    def Draw(self , screen):
        if self.mode == "normal":
            screen.blit(self.image,(self.position[0]*self.handler.PPM,self.position[1]*self.handler.PPM))

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
#Game class contains the basic things to run a single playroom
class Game:
    def __init__(self , screenSizeProduct = 1):
        self.logShown  = True
        self.PPM       = 20.0 * screenSizeProduct
        self.FPS       = 40.0
	self.ratio     = screenSizeProduct
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
        self.background  = 100,100,255
        
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
        self.AddLog("Starting game ...")

	self.scoreA = 0
	self.scoreB = 0
	self.time   = 0
	self.scoreImageA = None
	self.scoreImageB = None
	self.timeImages  = []
	self.pointsPoints= fonts.GetFont("VOM_30").render(":",1,(255,255,255))

	self.UpdateScoreAImage()
	self.UpdateScoreBImage()
	self.UpdateTimeImage()
	self.messages = dict()
   
	self.reference = 0
        self.stoped    = 0
        self.playingClock = False
        self.status      = "stoped"
        
        self.SetPlayerAName("Player A")
        self.SetPlayerBName("Player B")
        self.SetBackground(self.background)
    def Resize(self,width,height):
        #900x600
        ratioWidth  = width / 900.0  
        ratioHeight = height / 600.0
        if ratioWidth < ratioHeight:
            ratio = ratioWidth
        else:
            ratio = ratioHeight
        print "Ratio:",ratio
        self.PPM = 20.0 * ratio
        self.ratio = ratio
        self.CalculateHalfs()
        self.goal          = self.TranSize(Stage.goal)
	self.reverse_goal  = self.TranSize(Stage.reverse_goal)
	self.goalB         = self.TranSize(Stage.goalB)
	self.reverse_goalB = self.TranSize(Stage.reverse_goalB)
        self.GenerateBackgroundImage()     
        if self.playerAID != None:
            self.elements[self.playerAID].image = self.TranSize(heads[self.playerAHead])
        if self.playerBID != None:
            self.elements[self.playerBID].image = self.TranSize(heads[self.playerBHead])
    def SetPlayerAName(self,name):
        self.playerAName = name
        self.playerANameSurface = fonts.GetFont("VOM_20").render(self.playerAName,1,(255,255,255))
    def SetPlayerBName(self,name):
        self.playerBName = name
        self.playerBNameSurface = fonts.GetFont("VOM_20").render(self.playerBName,1,(255,255,255))
    def PlayBall(self):
        self.status = "wait4ball"
        self.statusStart = time.time()
    def AddMessage(self,color,font,content,key,position):
	self.messages[key] = {"color":color,"font":font,"content":content,"key":key,"position":position}
	self.messages[key]["image"] = self.GenerateImage(color,font,content)
    def DeleteMessage(self,key):
	del self.messages[key]
    def UpdateMessagePosition(self,key,postion):
	self.messages[key]["position"] = position
    def DrawMessages(self,screen):
	for msjk in self.messages.keys():
	    msj = self.messages[msjk]
	    self.DrawMessage(msj,screen)
    def DrawMessage(self,msj,screen):
	screen.blit(msj["image"],msj["position"])
    def DrawScore(self,screen):
	screen.blit(self.scoreImageA,(100,50))
	screen.blit(self.scoreImageB,(self.pixelWidth-100,50))
    def DrawNames(self,screen):
        screen.blit(self.playerANameSurface,(100-self.playerANameSurface.get_size()[0]/2,100))
	screen.blit(self.playerBNameSurface,(self.pixelWidth-100-self.playerBNameSurface.get_size()[0]/2,100))
    def UpdateScoreAImage(self):
	self.scoreImageA = fonts.GetFont("VOM_35").render(str(self.scoreA),1,(255,255,255))
    def UpdateScoreBImage(self):
	self.scoreImageB = fonts.GetFont("VOM_35").render(str(self.scoreB),1,(255,255,255))
    def UpdateTimeImage(self):
	ms = int(self.time % 100)
	s  = int((self.time/ 100 )%60) 
	m  = int(self.time / 100 / 60)

	msA = ms / 10
	msB = ms % 10
	sA  = s  / 10
	sB  = s  % 10
	mA  = m  / 10
	mB  = m  % 10
	self.timeImages = []
	self.RenderTime(mA)
	self.RenderTime(mB)
	self.RenderTime(":")
	self.RenderTime(sA)
	self.RenderTime(sB)
	self.RenderTime(":")
	self.RenderTime(msA)
	self.RenderTime(msB)
    def RenderTime(self,digit):
	self.timeImages.append( fonts.GetFont("VOM_30").render(str(digit),1,(255,255,255)) )
    def DrawTimeImage(self,screen):
	start_x = self.pixelWidth/2 - len(self.timeImages)*15
	for x in range(len(self.timeImages)):
	    screen.blit(self.timeImages[x],(start_x+30*x,200))
    def UpdateTime(self,time):
	self.time = time
	self.UpdateTimeImage()
    def SetClock(self,length = 1):
        self.length     = length
	self.reference  = time.time()*100
        self.playingClock = False
        self.stoped     = time.time()*100
    def StopClock(self):
        self.playingClock = False
        self.stoped = time.time()*100
    def ContinueClock(self):
        self.playingClock = True
        self.reference += time.time()*100 - self.stoped
    def UpdateClock(self):
        if self.playingClock:
            rest_time = self.length*60*100 - (time.time()*100 - self.reference)
 	    if rest_time > 0:
                self.UpdateTime( rest_time )
            else:
                self.UpdateTime(0)
                self.StopClock()
                self.status = "stoped"
                self.RemoveBall()
    def ScoreA(self):
        self.AddLog("Player A scores! "+str(self.scoreA)+"-"+str(self.scoreB))
        self.StopClock()
	self.scoreA += 1
	self.UpdateScoreAImage()
        self.status    = "wait4ball"
        self.statusStart = time.time()
    def ScoreB(self):
        self.AddLog("Player B scores! "+str(self.scoreA)+"-"+str(self.scoreB))
        self.StopClock()	
	self.scoreB += 1
        self.UpdateScoreBImage()
        self.status    = "wait4ball"
        self.statusStart = time.time()
    def GenerateImage(self,color,font,content):
	return fonts.GetFont(font).render(content,0,color)
    def NextId(self):
        self.idCount += 1
        return self.idCount
    def NextCountId(self):
        self.idShowCount += 1
        return self.idShowCount
    def AddLog(self,msg):
        if self.logShown:
            print msg
        self.Log.append(msg)
    def SetBackground(self,color):
        self.AddLog("Setting background color: "+str(color))
        self.background = color
        self.GenerateBackgroundImage()
    def GenerateBackgroundImage(self):
        self.backgroundImage = pygame.surface.Surface((self.pixelWidth,self.pixelHeight))
        self.backgroundImage.fill(self.background)
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
    def RemoveElement(self,id):
        self.AddLog("Element removed with id "+str(id))
        self.world.DestroyBody(self.elements[id].body)
        del self.elements[id]
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
        self.showThings[id] = ShowImage(self,image,position,mode)
    def DeleteShowThing(self,id):
        self.AddLog("Deleting show thing "+str(id))
        del self.showThings[id]
    def ChangeShowThingImage(self,id,image):
        self.showThings[id].image = image
    def ChangeShowThingPosition(self,id,position):
        self.showThings[id].position = position
    def AddBall(self):
        if self.ballID == None:
            self.AddLog("Adding ball ...")
        else:
            self.AddLog("Game has already a ball")
            return
        body         = self.world.CreateDynamicBody(bullet=True)
        circle       = body.CreateCircleFixture(radius=0.475, density=200, friction=0.1 ,restitution=0.95)
        element      = Element(self,body,(self.HalfWidth,self.HalfHeight),(0,10),"polygon",self.ballColor)
        #(self,handler,body,position,linearVelocity,drawMode,color=None,image=None)
        self.ballID  = self.NextId()
        self.AddElement(element,self.ballID)
    def RemoveBall(self):
        if self.ballID == None:
            self.AddLog("There is no ball")
            return
        else:
            self.AddLog("Removing ball ...")
        self.RemoveElement(self.ballID)
        self.ballID = None
    def ResetBall(self):
        self.AddLog("Reseting ball position ...")
        self.RemoveBall()
        self.AddBall()
    def AddPlayerA(self,headCode,name = "Player A"):
        self.SetPlayerAName(name)
        self.AddLog("Adding player A ...")
        self.playerAHead = headCode
        body = self.world.CreateDynamicBody()
        head = body.CreateCircleFixture(radius=1.3, density=400, friction=0)
        element = Element(self,body,(3,8),(0,0),"image",None,self.TranSize(heads[self.playerAHead]))
        self.playerAID = self.NextId()
        self.AddElement(element,self.playerAID)
        self.playerA = Player(element)
    def AddPlayerB(self,headCode,name = "Player B"):
        self.SetPlayerBName(name)
        self.AddLog("Adding player B ...")
        self.playerBHead = headCode
        body = self.world.CreateDynamicBody()
        head = body.CreateCircleFixture(radius=1.3,density=400,friction=0)
        element = Element(self,body,(42,8),(0,0),"image",None,self.TranSize(heads[self.playerBHead]))
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
    def AddPitch(self):
        self.AddLog("Adding pitch ...")
        #Creating Box2D elements
        bodyA = self.world.CreateStaticBody( position=( 1.5,8.25),shapes=polygonShape(box=(1.4, 0.2)),color=(0,0,0) )
        bodyB = self.world.CreateStaticBody( position=( 0.0, 0.0),shapes=polygonShape(box=(0.5,30.0)),color=(0,0,0) )
        bodyC = self.world.CreateStaticBody( position=(43.5,8.25),shapes=polygonShape(box=(1.5, 0.2)),color=(0,9,0) )
        bodyD = self.world.CreateStaticBody( position=(44.8,   0),shapes=polygonShape(box=(0.2,30.0)),color=(0,0,0) )
        bodyE = self.world.CreateStaticBody( position=(   0,   0),shapes=polygonShape(box=( 50, 1.0)),color=(0,0,0) )
        bodyF = self.world.CreateStaticBody( position=(   0,29.9),shapes=polygonShape(box=( 50, 0.1)),color=(0,0,0) )
        #Creating Common elements
        elementA = Element(self,bodyA,( 1.5,8.25),(0,0),"polygon",(0,255,0))
        elementB = Element(self,bodyB,(   0,   0),(0,0),"polygon",(0,0,0))
        elementC = Element(self,bodyC,(43.5,8.25),(0,0),"polygon",(0,255,0))
        elementD = Element(self,bodyD,(44.8,   0),(0,0),"polygon",(0,0,0))
        elementE = Element(self,bodyE,(   0,   0),(0,0),"polygon",(0,255,0))
        elementF = Element(self,bodyF,(   0,29.9),(0,0),"polygon",(0,0,0))
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
	self.goal          = self.TranSize(Stage.goal)
	self.reverse_goal  = self.TranSize(Stage.reverse_goal)
	self.goalB         = self.TranSize(Stage.goalB)
	self.reverse_goalB = self.TranSize(Stage.reverse_goalB)
        self.idGoalA = self.NextCountId()
        self.idGoalB = self.NextCountId()
        self.AddShowThing(self.idGoalA,self.goal ,(                 0,self.height-8.5))
        self.AddShowThing(self.idGoalB,self.reverse_goal,(self.width-3,self.height-8.5))
    def GoalEffectA(self):
        self.ChangeShowThingImage(self.idGoalA,self.goalB)
    def GoalEffectB(self):
        self.ChangeShowThingImage(self.idGoalB,self.reverse_goalB)
    def SetActions(self,actions,player):
        if player == "Player A":
            if self.playerA != None:
                self.playerA.UpdateActions(actions)
        elif player == "Player B":
            if self.playerB != None:
                self.playerB.UpdateActions(actions)
    def Loop(self):
        self.world.Step(self.TIME_STEP, 10, 10)
        self.UpdateGoals()
        self.UpdateClock()
        if self.status == "wait4ball":
             if time.time() - self.statusStart > 3:
                  self.AddLog("setting clock")
                  self.ResetBall()
                  self.status = "playing"
                  self.ContinueClock()
    def Draw(self,screen):
        screen.fill((0,0,0))
        partial = pygame.surface.Surface((self.pixelWidth,self.pixelHeight))
        partial.fill(self.background)
        for ELK in self.elements.keys():
            EL = self.elements[ELK]
            EL.Draw(partial)
        for EDK in self.showThings.keys():
            ED = self.showThings[EDK]
            ED.Draw(partial)
	self.DrawMessages(partial)
	self.DrawScore(partial)
        self.DrawTimeImage(partial)
        self.DrawNames(partial)
        screen.blit(partial,(screen.get_size()[0]/2-partial.get_size()[0]/2,screen.get_size()[1]/2-partial.get_size()[1]/2))
    def UpdateGoals(self):
        if self.ballID == None:
            return
        if self.GetElementPosition(self.ballID)[0] < 3 and self.GetElementPosition(self.ballID)[1] < 7.5:
            if self.counterGoalA == 0:
                self.showThings[self.idGoalA].image = self.goalB
                self.DivideElementLinearVelocity(self.ballID,4)
                if self.status == "playing":
                    self.ScoreB()
            self.counterGoalA = 40
            if self.targetAction != None:
                self.targetAction.ScoreA()

        if self.GetElementPosition(self.ballID)[0] > 42 and self.GetElementPosition(self.ballID)[1] < 7.5:
            if self.counterGoalB == 0:
                self.showThings[self.idGoalB].image = self.reverse_goalB
                self.DivideElementLinearVelocity(self.ballID,4)
                if self.status == "playing":
                    self.ScoreA()
            self.counterGoalB = 40
            if self.targetAction != None:
                self.targetAction.ScoreB()
        if self.counterGoalA > 0:
            self.counterGoalA -= 1
        else:
             self.showThings[self.idGoalA].image = self.goal
        if self.counterGoalB > 0:
            self.counterGoalB -= 1
        else:
            self.showThings[self.idGoalB].image = self.reverse_goal
    def PrintLog(self):
        for x in range(len(self.Log)):
            print "Log "+str(x)+" "+self.Log[x]
    def TranSize(self,image):
	return pygame.transform.scale(image,(image.get_size()[0]*self.ratio,image.get_size()[1]*self.ratio))
    
def get_key_actions(keys):
    return {"up":keys[pygame.K_UP],"down":keys[pygame.K_DOWN],"left":keys[pygame.K_LEFT],"right":keys[pygame.K_RIGHT]}
def get_alternative_key_actions(keys):
    return {"up":keys[pygame.K_w],"down":keys[pygame.K_s],"left":keys[pygame.K_a],"right":keys[pygame.K_d]}

def main():
    screen = pygame.display.set_mode((900*3/4,600*3/4),HWSURFACE|DOUBLEBUF|RESIZABLE)
    game   = Game(0.75)
    game.AddPitch()
    game.AddPlayerA("head A","Newtonis")
    game.AddPlayerB("head B","Penguin")
    game.SetClock(1.5)
    game.PlayBall()
    clock = pygame.time.Clock()
    continuar = True
    
    while continuar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuar = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    continuar = False
            	elif event.key == pygame.K_s:
                    game.StopClock()
                elif event.key == pygame.K_c:
                    game.ContinueClock()
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                width , height = event.dict['size']
                print width,height
                game.Resize(width,height)
        keys = pygame.key.get_pressed()
        game.SetActions(get_key_actions(keys),"Player B")
        game.SetActions(get_alternative_key_actions(keys),"Player A")
        game.Loop()
        game.Draw(screen)
	#screen.blit(pygame.transform.scale(preScreen,screen.get_size()),(0,0))
        pygame.display.flip()
        clock.tick(40)

    #game.PrintLog()
if __name__ == "__main__":
    main()
