__author__ = 'newtonis'
import pygame

directory = "images/"

class HeadsImages:
    headA = pygame.transform.scale( pygame.image.load(directory+"cabeza1.png") , (60,60) )
    headB = pygame.transform.scale( pygame.image.load(directory+"cabeza3.png") , (50,50) )

heads = { \
    "head A":HeadsImages.headA, \
    "head B":HeadsImages.headB  \
}

class Feet:
    feetA = pygame.image.load(directory + "botin.png")

class Stage:
    goal  = pygame.image.load(directory + "goal.png")
    goalB = pygame.image.load(directory + "goal2.png")

    reverse_goal = pygame.transform.flip(goal  , True , False)
    reverse_goalB= pygame.transform.flip(goalB , True , False)