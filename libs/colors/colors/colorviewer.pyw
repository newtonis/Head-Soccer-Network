#-------------------------------------------------------------------------------
# Name:        Colors
# Purpose:     Color library for Python/Pygame
#
# Author:      Joshua Smith
#
# Created:     08/29/2012
# Copyright:   (c) Joshua Smith 2012
# Licence:     GNU Public License
#-------------------------------------------------------------------------------
import pygame, sys
from pygame.locals import *

#----------Start of colors----------#
red1=50,0,0
red2=75,0,0
red3=100,0,0
red4=125,0,0
red5=150,0,0
red6=175,0,0
red7=200,0,0
red8=225,0,0
red9=255,0,0
red10=255,150,150
reds = [red1,red2,red3,red4,red5,
        red6,red7,red8,red9,red10]
#-----------------------------------#
green1=0,50,0
green2=0,75,0
green3=0,100,0
green4=0,125,0
green5=0,150,0
green6=0,175,0
green7=0,200,0
green8=0,225,0
green9=0,255,0
green10=150,255,150
greens = [green1,green2,green3,green4,green5,
        green6,green7,green8,green9,green10]
#-----------------------------------#
blue1=0,0,50
blue2=0,0,75
blue3=0,0,100
blue4=0,0,125
blue5=0,0,150
blue6=0,0,175
blue7=0,0,200
blue8=0,0,225
blue9=0,0,255
blue10=125,125,255
blues = [blue1,blue2,blue3,blue4,blue5,
        blue6,blue7,blue8,blue9,blue10]
#-----------------------------------#
purple1=50,0,50
purple2=75,0,75
purple3=100,0,100
purple4=125,0,125
purple5=150,0,150
purple6=175,0,175
purple7=200,0,200
purple8=225,0,225
purple9=240,0,240
purple10=255,150,255
purples = [purple1,purple2,purple3,purple4,purple5,
        purple6,purple7,purple8,purple9,purple10]
#-----------------------------------#
brown1=50,25,0
brown2=75,38,0
brown3=100,50,0
brown4=125,62,0
brown5=150,75,0
brown6=175,88,0
brown7=200,101,0
brown8=225,114,0
brown9=250,127,0
brown10=255,140,25
browns = [brown1,brown2,brown3,brown4,brown5,
        brown6,brown7,brown8,brown9,brown10]
#-----------------------------------#
orange1=150,75,0
orange2=175,80,0
orange3=200,85,0
orange4=225,90,0
orange5=235,95,0
orange6=245,100,0
orange7=255,105,0
orange8=255,125,0
orange9=255,150,50
orange10=255,200,100
oranges = [orange1,orange2,orange3,orange4,orange5,
           orange6,orange7,orange8,orange9,orange10]
#-----------------------------------#
yellow1=75,75,0
yellow2=100,100,0
yellow3=125,125,0
yellow4=150,150,0
yellow5=175,175,0
yellow6=200,200,0
yellow7=225,225,0
yellow8=250,250,0
yellow9=255,255,100
yellow10=255,255,150
yellows = [yellow1,yellow2,yellow3,yellow4,yellow5,
        yellow6,yellow7,yellow8,yellow9,yellow10]
#-----------------------------------#
cyan1=0,50,50
cyan2=0,75,75
cyan3=0,100,100
cyan4=0,125,125
cyan5=0,150,150
cyan6=0,175,175
cyan7=0,200,200
cyan8=0,225,225
cyan9=0,255,255
cyan10=150,255,255
cyans = [cyan1,cyan2,cyan3,cyan4,cyan5,
        cyan6,cyan7,cyan8,cyan9,cyan10]
#-----------------------------------#
gray1=25,25,25
gray2=50,50,50
gray3=75,75,75
gray4=100,100,100
gray5=125,125,125
gray6=150,150,150
gray7=175,175,175
gray8=200,200,200
gray9=225,225,225
gray10=245,245,245
grays = [gray1,gray2,gray3,gray4,gray5,
        gray6,gray7,gray8,gray9,gray10]
#-----------------------------------#
white=255,255,255
black=0,0,0
neutrals = [white,black]

available_colors=[reds,oranges,yellows,greens,cyans,
                blues,purples,browns,grays,neutrals]
#-----------End of colors-----------#
        
def Set_Colors(available_colors):
    counter = 0
    colors = []
    for i in available_colors:
        for i in i:
            colors.append(i)

    Pre_Build(colors)

def Pre_Build(colors):
    screen = pygame.display.set_mode((250,250))
    pygame.display.set_caption('Colors ~ Joshua Smith')
    screen.fill((colors[50]))
    x, y = 0,0
    for i in colors:
        pygame.draw.rect(screen, i, Rect((x,y), (25,25)))
        x += 25
        if x == 250:
            x = 0
            y +=25
            
    pygame.display.update()
    main()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    

Set_Colors(available_colors)
