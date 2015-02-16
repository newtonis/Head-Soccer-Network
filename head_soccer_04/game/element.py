__author__ = 'ariel'

import pygame

import Box2D
from Box2D.b2 import *
from colors import *
from images import *

POLYGON2D , \
IMAGE = range(2)

RIGHT , \
LEFT  , \
CENTER = range(3)

class Element:
    def __init__(self, way ,body , handler , color = ball, type = POLYGON2D):
        self.body  = body
        self.type  = type
        self.color = color
        self.handler = handler
        self.way   = way
    def draw(self,screen):
        if self.type == POLYGON2D:
            for fixture in self.body.fixtures:
                fixture.shape.draw(self.body, fixture , self.handler , self.color)
        elif self.type == IMAGE:
            for fixture in self.body.fixtures:
                fixture.shape.draw(self.body, fixture , self.handler , self.color)
            screen.blit(self.image , (self.body.position[0]*self.handler.PPM - 20,(screen.get_size()[1]-self.body.position[1]*self.handler.PPM)  -20 ) )
    def update(self):
        pass
    def GetCode(self):
        if self.way == "ball":
            return {"id":self.id,"type":self.way,"position":[self.body.position[0],self.body.position[1]],"linearVelocity":[self.body.linearVelocity[0],self.body.linearVelocity[1]]}
        else:
            return {"type":self.way}

J1 ,\
J2 ,\
MANUAL = range(3)

class Head(Element):
    def __init__(self , pos , head_image , handler , mode = MANUAL):
        self.mode = mode
        self.head = head_image
        body = handler.world.CreateDynamicBody(position=pos )
        head= body.CreateCircleFixture(radius=1.3, density=400, friction=0, )
        Element.__init__(self, "head" ,body , ball , IMAGE )

        #self.body_botin = handler.world.CreateDynamicBody(position=pos ,color=(0,0,0) , density=0 )
        #self.body_botin.preventRotation=True
        #botin= self.body_botin.CreatePolygonFixture(box=(0.5,0.25), density=20, friction=0,restitution=0.8 )

        if head_image == "head A":
            self.image = HeadsImages.headA
        elif head_image == "head B":
            self.image = HeadsImages.headB

        self.vv = -1.0
        self.enabled = False
        self.handler = handler
    def SetLinearVelocity(self , velocity):
        self.body.linearVelocity = velocity
    def update(self):
        #self.move_pressed()
        pass
    def draw(self,screen):
        if self.mode == J2:
            self.move_pressed()
        elif self.mode == J1:
            self.move_pressedB()
        #screen.blit(self.image , (self.body.position[0]*handler.PPM - 30*1.3,(screen.get_size()[1]-self.body.position[1]*handler.PPM)  -30*1.3 ) )
        #for fixture in self.body.fixtures:
        #    fixture.shape.draw(self.body, fixture , handler , self.color)
        screen.blit(self.image , (self.body.position[0]*self.handler.PPM - 30,(screen.get_size()[1]-self.body.position[1]*self.handler.PPM)  -30 ) )
        #for fixture in self.body_botin.fixtures:
        #    fixture.shape.draw(self.body_botin, fixture , handler , self.color)

    def movement(self , move , jump):

        if move == 1:
            v_line = 10
            #self.body.linearVelocity=(90,16.445)
        elif move == -1:
            v_line = -10
            #self.body.linearVelocity=(90,16.445)
        elif move == 0:
            v_line = 0

        if jump == True and self.body.position[1] < 2.5:
            h_line = 15
        else:
            h_line = 0

        if self.enabled:
            SpeedBotin = 5
        else:
            SpeedBotin = 0
        self.body.linearVelocity=(v_line ,  self.body.linearVelocity[1]+h_line)
        #self.body_botin.linearelocity=(v_line ,  self.body.linearVelocity[1]+h_line)
    def move_pressed(self):
        keys = pygame.key.get_pressed()

        move_x = 0
        if keys[pygame.K_RIGHT]:
            move_x += 1
        if keys[pygame.K_LEFT]:
            move_x -= 1

        self.movement( move_x , keys[pygame.K_UP])

        if keys[pygame.K_SPACE] and self.enabled == False:
            self.enabled = True
        elif not keys[pygame.K_SPACE]:
            self.enabled = False
            self.vv = -1.0
    def move_pressedB(self):
        keys = pygame.key.get_pressed()

        move_x = 0
        if keys[pygame.K_d]:
            move_x += 1
        if keys[pygame.K_a]:
            move_x -= 1

        self.movement( move_x , keys[pygame.K_w])

        if keys[pygame.K_p] and self.enabled == False:
            self.enabled = True
        elif not keys[pygame.K_p]:
            self.enabled = False
            self.vv = -1.0
    def move_manual(self , actions):
        move_x = 0
        if actions["right"]:
            move_x += 1
        if actions["left"]:
            move_x -= 1

        self.movement( move_x , actions["jump"])

        if actions["kick"] and self.enabled == False:
            self.enabled = True
        elif not actions["kick"]:
            self.enabled = False
            self.vv = -1.0
    def GetCode(self):
        return {"type":self.way,"position":[self.body.position[0],self.body.position[1]],"linearVelocity":[self.body.linearVelocity[0],self.body.linearVelocity[1]],"head":self.head,"id":self.id}

NORMAL , \
SCORED_A , \
FINAL = range(3)
class Goals(Element):
    def __init__(self , side , handler):
        self.way = "goals"
        self.color = goal


        self.bodyA = handler.world.CreateStaticBody( position=(1.5,8.25),shapes=polygonShape(box=(1.5,0.2)),color=(0,0,0) )
        self.bodyB = handler.world.CreateStaticBody( position=(0,0),shapes=polygonShape(box=(0.5,30)),color=(0,0,0) )

        self.bodyC = handler.world.CreateStaticBody( position=(43.5,8.25),shapes=polygonShape(box=(1.5,0.2)),color=(0,0,0) )
        self.bodyD = handler.world.CreateStaticBody( position=(44.8,0),shapes=polygonShape(box=(0.2,30)),color=(0,0,0) )

        self.handler = handler

        self.bodies = []
        self.bodies.append( self.bodyA )
        self.bodies.append( self.bodyB )
        self.bodies.append( self.bodyC )
        self.bodies.append( self.bodyD )
        self.status  = NORMAL
        self.statusB = NORMAL
        self.counter = 0
    def draw(self , screen):

        W,H = screen.get_size()
        if self.status == NORMAL:
            screen.blit(Stage.goal,(0,H-170))
        elif self.status == SCORED_A:
            screen.blit(Stage.goalB,(0,H-170))
            self.counter += 1
            if self.counter > 10:
                self.status = NORMAL
        if self.statusB == NORMAL:
            screen.blit(Stage.reverse_goal , (840,H-170))
        elif self.statusB == SCORED_A:
            screen.blit(Stage.reverse_goalB,(840,H-170))
            self.counter += 1
            if self.counter > 10:
                self.statusB = NORMAL
        #for body in self.bodies:
        #    for fixture in body.fixtures:
        #        fixture.shape.draw(body, fixture , self.handler , self.color)
    def scoreGoalA(self):
        self.status = SCORED_A
        self.counter = 0
    def scoreGoalB(self ):
        self.statusB = SCORED_A
        self.counter = 0
    def GetCode(self):
        return {"type":"no add"}