__author__ = 'ariel'
from colors import *
from Box2D.b2 import *
import pygame

# Let's play with extending the shape classes to draw for us.
def my_draw_polygon(polygon, body, fixture , handler ,color ):
    vertices=[(body.transform*v)*handler.PPM for v in polygon.vertices]
    vertices=[(v[0], handler.SCREEN_HEIGHT-v[1]) for v in vertices]
    pygame.draw.polygon(handler.screen, colors[color], vertices)
polygonShape.draw=my_draw_polygon

def my_draw_circle(circle, body, fixture , handler ,color):
    position=body.transform*circle.pos*handler.PPM
    position=(position[0], handler.SCREEN_HEIGHT-position[1])
    pygame.draw.circle(handler.screen, colors[color], [int(x) for x in position], int(circle.radius*handler.PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.
circleShape.draw=my_draw_circle