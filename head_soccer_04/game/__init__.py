__author__ = 'ariel'

import pygame
import Box2D
#from Box2D.b2 import *
from math import *
import test1
from colors import *
from draw import *
from element import *
import images
NORMAL , \
END = range(2)

class Game_handler:
    def __init__(self , size, caption):
        self.status = NORMAL
        self.screen = pygame.display.set_mode(size)
        self.clock  = pygame.time.Clock()

        self.PPM                              = 20.0 # pixels per meter
        self.TARGET_FPS                       = 40.0
        self.TIME_STEP                        = 1.0 / self.TARGET_FPS
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = size

        self.world = world(gravity=(0,-30),doSleep=True)

        self.elements = dict()
        pygame.display.set_caption(caption)

        self.ball = None
        self.goal = None
        self.targetAction = None
    def SetTarget(self,target):
        self.targetAction = target
    def SetFps(self,fps):
        self.TARGET_FPS                       = float(fps)
        self.TIME_STEP                        = 1.0 / float(self.TARGET_FPS)
    def NextId(self):
        self.id += 1
        return self.id
    def clear(self):
        self.screen.fill((100,100,255))
    def refresh(self):
        pygame.display.flip()
        self.clock.tick(self.TARGET_FPS)
    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.status = END
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.status = END
                if event.key == pygame.K_r:
                    self.__init__((900,600),"Testeo bola")
                    test1.add_test(self)
    def exit(self):
        return self.status == END
    def draw(self):
        # Draw the world
        for ELK in self.elements.keys():
            EL = self.elements[ELK]
            EL.draw(self.screen)
            #body = EL.body
            #for fixture in body.fixtures:
            #    fixture.shape.draw(body, fixture , self , EL.color , self.screen)

    def update(self):
        self.world.Step(self.TIME_STEP, 10, 10)
        self.update_goals()
    def update_goals(self):
        if self.ball != None:
            if self.ball.body.position[0] < 3 and self.ball.body.position[1] < 7.5:
                if self.goal.status == NORMAL:
                    self.ball.body.linearVelocity[0] /= 4
                    self.ball.body.linearVelocity[1] /= 4
                self.goal.scoreGoalA()
                if self.targetAction != None:
                    self.targetAction.ScoreA()

            if self.ball.body.position[0] > 42 and self.ball.body.position[1] < 7.5:
                if self.goal.statusB == NORMAL:
                    self.ball.body.linearVelocity[0] /= 4
                    self.ball.body.linearVelocity[1] /= 4
                self.goal.scoreGoalB()
                if self.targetAction != None:
                    self.targetAction.ScoreB()

    def add_element(self , element , id):
        element.id = id
        self.elements[id] = element
        return element
    def delete_element(self,id):
        self.world.DestroyBody(self.elements[id].body)
        del self.elements[id]
    def add_pitch(self , idA , idB , idC):
        self.add_element( Element( "wall",self.world.CreateStaticBody( position=(0,0),shapes=polygonShape(box=(50,1)),color=(0,0,0) ), self , base ) , idA )
        self.add_element( Element( "wall",self.world.CreateStaticBody(position=(0,29.9) ,shapes=polygonShape(box=(50,0.1)),color=(0,0,0) ), self ,goal) , idB)
        goals = Goals(0,self)
        self.add_element(goals, idC)
        self.goal = goals
    def add_ball(self , id , side):
        if side == 1:
            vel = -5,10
        elif side == 2:
            vel =  5,10
        e=self.add_element(Element("ball",self.world.CreateDynamicBody(position=(20,2) , linearVelocity=vel , bullet=True) , self  , ball),id)
        circle=e.body.CreateCircleFixture(radius=0.475, density=200, friction=0.1 ,restitution=0.95)
        self.ball = circle
        return e
    def add_player_A(self , id):
        return self.add_element(Head((3,1),"head A", self ),id)
    def add_player_B(self , id):
        return  self.add_element(Head((30,1),"head B" , self ),id)



    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.
