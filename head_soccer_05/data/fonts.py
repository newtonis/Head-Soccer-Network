__author__ = 'ariel'

import pygame
pygame.font.init()

def LoadFont(file,size):
    return pygame.font.Font("fonts/"+file,size)

class CTProLamina:
    c20 = LoadFont("CT ProLamina.ttf",20)
    c22 = LoadFont("CT ProLamina.ttf",22)
    c30 = LoadFont("CT ProLamina.ttf",30)
    c40 = LoadFont("CT ProLamina.ttf",40)
