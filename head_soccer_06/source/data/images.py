__author__ = 'ariel'
import pygame
import math
import glob

def LoadImage(directory):
    return pygame.image.load("images/"+directory)

def LoadHead(directory):
    head = pygame.transform.scale ( LoadImage(directory) ,(60,60))
    reverse_head = pygame.transform.flip(head,True,False)

    return head, reverse_head

def LoadDirBoth(directory):
    files = sorted(glob.glob("images/"+directory+"/*"))
    result = []
    for file in files:
        image = pygame.image.load(file)
        Rimage = pygame.transform.flip(image,True,False)
        result.append([image,Rimage])
    return result
class Backgrounds:
    back1 = LoadImage("back1.png")
    back2 = LoadImage("back2.png")
    back3 = LoadImage("back3.png")
    back4 = LoadImage("back4.png")
    back5 = LoadImage("back5.png")
    back6 = LoadImage("back6.png")

class Heads:
    feetA = LoadImage("botin.png")

    goal  = LoadImage("goal.png")
    goalB = LoadImage("goal2.png")

    goalClassic = LoadDirBoth("goalA")

    reverse_goal = pygame.transform.flip(goal  , True , False)
    reverse_goalB= pygame.transform.flip(goalB , True , False)

    codes = { \
        "head A":LoadHead("cabeza1.png"), \
        "head B":LoadHead("cabeza2.png"), \
        "head C":LoadHead("cabeza3.png"), \
        "head D":LoadHead("cabeza4.png"),  \
        "goal":goal,\
        "goalB":goalB,\
        "rgoal":reverse_goal,\
        "rgoalB":reverse_goalB, \
        "ORTstadium":LoadImage("ORT_staidium_v0.jpg")
    }

    heads = [ "head A","head B","head C","head D" ]
class Extras:
    void = LoadImage("Vacio.png")

class Checkbox:
    checkbox = LoadImage("checkbox.png")
    checkbox_checked = LoadImage("checkbox_checked.png")

def FillWithBack(surface,back):
    for x in range(surface.get_size()[0]):
        surface.blit(back,(x,0))

def GetInter(initial_color,end_color,position,total):
    red , green , blue  = initial_color
    red2, green2, blue2 = end_color

    red_variant = abs(red-red2) * (float(position) / float(total))
    green_variant = abs(green-green2) * (float(position) / float(total))
    blue_variant  = abs(blue-blue2) * (float(position) / float(total))

    if red2 > red:
        final_red = red + red_variant
    else:
        final_red = red - red_variant
    if green2 > green:
        final_green = green + green_variant
    else:
        final_green = green - green_variant
    if blue2 > blue:
        final_blue = blue + blue_variant
    else:
        final_blue = blue - blue_variant

    return int(final_red),int(final_green),int(final_blue)

def FillWithColor(surface,initial_color,end_color):
    for x in range(0,surface.get_size()[1]):
        color = GetInter(initial_color,end_color,surface.get_size()[1]-x,surface.get_size()[1])
        #print color
        back = pygame.surface.Surface((surface.get_size()[0],1))
        back.fill(color)
        surface.blit(back,(0,x))

def Testing():
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Test")
    surface = pygame.surface.Surface((800,600))
    FillWithColor(surface,(255,0,0),(0,0,255))

    continuar = True
    while continuar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuar = False
        screen.fill((255,255,255))
        screen.blit(surface,(0,0))
        pygame.display.update()

if __name__ == "__main__":
    Testing()