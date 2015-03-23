__author__ = 'Dylan'
import pygame
import math
from addBorder import AddBorder2
import source.data.images as img
import pygame.gfxdraw

def roundNumber(number):
    decimal = number - math.floor(number)
    if decimal < 0.5:
        return math.floor(number)
    else:
        return math.ceil(number)

def equation(x,radius):
    if x == 0:
        return radius-1
    radius = float(radius)
    return int(roundNumber(radius - math.sqrt( 2*radius*x - x*x )))

def equationB(x,radius):
    if x == 0:
        return radius-1
    radius = float(radius)
    return int(roundNumber(radius + math.sqrt( 2*radius*x - x*x )))

def circleEquation(x,radius):
    A = equation (x,radius)
    B = equationB(x,radius)
    if A == B:
        return [A]
    else:
        return [A,B]

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def NoFilledRhombus(Color,Radius):
    VoidImage = img.Extras.void
    TempSurf = pygame.transform.scale(VoidImage,(Radius*2,Radius*2))
    pixel = pygame.Surface((1,1))
    pixel.fill(Color)

    xc = Radius
    yc = Radius
    x = Radius
    y = 0
    cd2= 0

    TempSurf.blit(pixel,(xc-Radius, yc))
    TempSurf.blit(pixel,(xc+Radius, yc))
    TempSurf.blit(pixel,(xc, yc-Radius))
    TempSurf.blit(pixel,(xc, yc+Radius))

    while (x > y):
        x -= 1
        y += 1
        cd2 -= x - y
        if (cd2 < 0):
            #x += 1
            cd2 += x

        TempSurf.blit(pixel,(xc-x, yc-y))
        TempSurf.blit(pixel,(xc-y, yc-x))
        TempSurf.blit(pixel,(xc+y, yc-x))
        TempSurf.blit(pixel,(xc+x, yc-y))
        TempSurf.blit(pixel,(xc-x, yc+y))
        TempSurf.blit(pixel,(xc-y, yc+x))
        TempSurf.blit(pixel,(xc+y, yc+x))
        TempSurf.blit(pixel,(xc+x, yc+y))

    return TempSurf


def PerfectCircle(Color, Radius):
    VoidImage = img.Extras.void
    TempSurf = pygame.transform.scale(VoidImage,(Radius*2,Radius*2))
    for q in range(Radius*2):
        Points = circleEquation(q,Radius)
        if len(Points) == 1:
            SurfaceAct = pygame.Surface((0,0))
            PosAct = [q,Points[0]]
        elif len(Points) == 2:
            Disf = Points[1]-Points[0]
            SurfaceAct = pygame.Surface((1,Disf))
            PosAct = [q,Points[0]]
        SurfaceAct.fill(Color)
        TempSurf.blit(SurfaceAct,PosAct)
    return TempSurf

def CircleBorderRectangle(tam=(0,0),Color=(0,0,0),Radio=0,Transparecy=False, BorderSize = 1, Opacity = 255,Exceptions = []):
    VoidImage = img.Extras.void
    Surface = pygame.transform.scale(VoidImage,tam)
    Position = (-1,0)
    if Transparecy == False:
        #  Rectangles of the middle
        MenorX = False
        MenorY = False
        SizeRectVer = [tam[0]-Radio*2,tam[1]]
        SizeRectHor = [tam[0],tam[1]-Radio*2]
        if tam[0] - Radio*2 < 0:
            MenorX = True
            SizeRectVer[0] = 0
        if tam[1] - Radio*2 < 0:
            MenorY = True
            SizeRectHor[1] = 0
        pygame.draw.rect(Surface, Color, (Position[0]+Radio,Position[1],SizeRectVer[0],SizeRectVer[1]))
        pygame.draw.rect(Surface, Color, (Position[0],Position[1]+Radio,SizeRectHor[0],SizeRectHor[1]))
        Positions = [
            #  Borde izquierda superior
            [Position,Position],
            #  Borde derecha superior
            [[Position[0]+tam[0]-Radio*2, Position[1]], [Position[0]+tam[0]-Radio, Position[1]]],
            #  Borde izquierda inferior
            [[Position[0], Position[1]+tam[1]-Radio*2],[Position[0], Position[1]+tam[1]-Radio]],
            #  Borde derecha inferior
            [[Position[0]+tam[0]-Radio*2, Position[1]+tam[1]-Radio*2],[Position[0]+tam[0]-Radio, Position[1]+tam[1]-Radio]]
        ]
        Size = [Radio*2, Radio*2]
        for q in range(4):
            Circle = True
            for w in range(len(Exceptions)):
                if Exceptions[w] == q:
                    Circle = False
                    break
            if Circle:
                Surf = PerfectCircle(Color, Radio)
                Surface.blit(Surf,[Positions[q][0][0], Positions[q][0][1]])
            else:
                SizeAct = [0,0]
                Dibujar = True
                if not MenorX:
                    SizeAct[0] = Radio
                else:
                    Dibujar = False
                if not MenorY:
                    SizeAct[1] = Radio
                else:
                    Dibujar = False
                if Dibujar:
                    pygame.draw.rect(Surface,Color,[Positions[q][1][0], Positions[q][1][1], SizeAct[0], SizeAct[1]])#pygame.draw.rect(Surface,Color,[Positions[q][1][0], Positions[q][1][1], SizeAct[0], SizeAct[1]])
    else:
        pi = 3.14159265359
        Radio1 = Radio*2
        PosArcs = [
            [Position,Position],
            [[Position[0]+tam[0]-Radio1,Position[1]],[Position[0]+tam[0]-Radio,Position[1]]],
            [[Position[0],Position[1]+tam[1]-Radio1],[Position[0],Position[1]+tam[1]-Radio]],
            [[Position[0]+tam[0]-Radio1,Position[1]+tam[1]-Radio1],[Position[0]+tam[0]-Radio,Position[1]+tam[1]-Radio]]
        ]
        SizeArcs = [Radio1,Radio1]
        RangeArcs = [
            [pi/2, pi],
            [0, pi/2],
            [pi, 1.5*pi],
            [1.5*pi, 2*pi]
        ]
        Borders = [
            [BorderSize,BorderSize,0,0],
            [BorderSize,0,BorderSize,0],
            [0,BorderSize,0,BorderSize],
            [0,0,BorderSize,BorderSize]
        ]
        for q in range(4):
            Circle = True
            for w in range(len(Exceptions)):
                if Exceptions[w] == q:
                    Circle = False
                    break
            if Circle:
                pygame.gfxdraw.arc(Surface,Position[0]+tam[0],Position[1],Radio,int(RangeArcs[q][0]/pi*180),int(RangeArcs[q][1]/pi*180),Color)
                #pygame.draw.arc(Surface, Color, [PosArcs[q][0][0]+1, PosArcs[q][0][1], SizeArcs[0], SizeArcs[1]], RangeArcs[q][0], RangeArcs[q][1], BorderSize)
            else:
                SurfaceAct = pygame.transform.scale(VoidImage,(Radio,Radio))
                AddBorder2(SurfaceAct, Borders[q][0], Borders[q][1], Borders[q][2], Borders[q][3], Color)
                Surface.blit(SurfaceAct,(PosArcs[q][1][0]+1,PosArcs[q][1][1]))
        pygame.draw.line(Surface, Color, (Position[0]+Radio,Position[1]), (Position[0]+tam[0]-Radio,Position[1]), BorderSize)
        pygame.draw.line(Surface, Color, (Position[0]+1,Position[1]+Radio), (Position[0]+1,Position[1]+tam[1]-Radio), BorderSize)
        pygame.draw.line(Surface, Color, (Position[0]+tam[0]-BorderSize+1,Position[1]+Radio), (Position[0]+tam[0]-BorderSize+1,Position[1]+tam[1]-Radio), BorderSize)
        pygame.draw.line(Surface, Color, (Position[0]+Radio,Position[1]+tam[1]-BorderSize), (Position[0]+tam[0]-Radio,Position[1]+tam[1]-BorderSize), BorderSize)
    Surface.fill((255,255,255,Opacity),None,pygame.BLEND_RGBA_MULT)
    return Surface