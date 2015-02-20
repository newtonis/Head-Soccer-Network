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

class AldoTheApache:
    c20 = LoadFont("AldotheApache.ttf",20)
    c22 = LoadFont("AldotheApache.ttf",22)
    c30 = LoadFont("AldotheApache.ttf",30)
    c40 = LoadFont("AldotheApache.ttf",40)

class BebasNeue:
    c15 = LoadFont("BebasNeue.ttf",15)
    c20 = LoadFont("BebasNeue.ttf",20)
    c22 = LoadFont("BebasNeue.ttf",22)
    c25 = LoadFont("BebasNeue.ttf",25)
    c30 = LoadFont("BebasNeue.ttf",30)
    c40 = LoadFont("BebasNeue.ttf",40)
    c50 = LoadFont("BebasNeue.ttf",50)
    c60 = LoadFont("BebasNeue.ttf",60)
    array = [c15,c20,c22,c25,c30,c40,c50,c60]

class PowerChord:
    c20 = LoadFont("PowerChord.ttf",20)
    c22 = LoadFont("PowerChord.ttf",22)
    c30 = LoadFont("PowerChord.ttf",30)
    c40 = LoadFont("PowerChord.ttf",40)

class MotionControl:
    c20 = LoadFont("MotionControl-Bold.ttf",20)
    c22 = LoadFont("MotionControl-Bold.ttf",22)
    c25 = LoadFont("MotionControl-Bold.ttf",25)
    c30 = LoadFont("MotionControl-Bold.ttf",30)
    c40 = LoadFont("MotionControl-Bold.ttf",40)
    c50 = LoadFont("MotionControl-Bold.ttf",50)
    array = [c20,c22,c25,c30,c40,c50]

class PixelSplitter:
    c11 = LoadFont("PixelSplitter-Bold.ttf",11)
    c12 = LoadFont("PixelSplitter-Bold.ttf",12)
    c13 = LoadFont("PixelSplitter-Bold.ttf",13)
    c14 = LoadFont("PixelSplitter-Bold.ttf",14)
    c15 = LoadFont("PixelSplitter-Bold.ttf",15)
    c20 = LoadFont("PixelSplitter-Bold.ttf",20)

class Absender:
    c20 = LoadFont("absender1.ttf",20)
    c30 = LoadFont("absender1.ttf",30)
    c40 = LoadFont("absender1.ttf",40)
    c50 = LoadFont("absender1.ttf",50)
    c80 = LoadFont("absender1.ttf",80)

class BoomBox:
    class Original:
        c20 = LoadFont("BOOMBOX.TTF",20)
        c40 = LoadFont("BOOMBOX.TTF",40)
        c50 = LoadFont("BOOMBOX.TTF",50)
        c60 = LoadFont("BOOMBOX.TTF",60)
        c80 = LoadFont("BOOMBOX.TTF",80)
    class NewVersion:
        c20 = LoadFont("boombox2.ttf",20)
        c40 = LoadFont("boombox2.ttf",40)
        c50 = LoadFont("boombox2.ttf",50)
        c60 = LoadFont("boombox2.ttf",60)
        c80 = LoadFont("boombox2.ttf",80)