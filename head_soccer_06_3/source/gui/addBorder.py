__author__ = 'ariel'

##### El objetivo de este archvio es brindar una funcion para facilmente agregar bordes a una superficie####

import pygame

def AddBorder(surface,b=1,color=(0,0,0),special=True):
    if not surface.get_colorkey():
        surface.set_colorkey((0,0,1))
    width,height = surface.get_size()

    b1Surface = pygame.surface.Surface((width,b))
    b2Surface = pygame.surface.Surface((b,height))

    b1Surface.fill(color)
    b2Surface.fill(color)

    surface.blit(b1Surface,(0,0))
    surface.blit(b2Surface,(0,0))
    surface.blit(b1Surface,(0,height-b))
    surface.blit(b2Surface,(width-b,0))

    if special:
        white = pygame.surface.Surface((1,1))
        white.fill(surface.get_colorkey())
        surface.blit(white,(0,0))
        surface.blit(white,(0,height-1))
        surface.blit(white,(width-1,0))
        surface.blit(white,(width-1,height-1))

def SpecialAddBorder(surface,borders,color=(0,0,0)):
    for n in borders:
        pygame.draw.line(surface,color,n[0],n[1])

def AddBorder2(surface,top=1,left=1,right=1,down=1,color=(0,0,0)):
    up_size = surface.get_size()[0]
    side_size = surface.get_size()[1]
    pygame.draw.line(surface,color,(0,0),(up_size,0),top)
    pygame.draw.line(surface,color,(0,0),(0,side_size),left)
    pygame.draw.line(surface,color,(up_size-right,0),(up_size-right,side_size),right)
    pygame.draw.line(surface,color,(0,side_size-down),(up_size,side_size-down),down)
    return surface