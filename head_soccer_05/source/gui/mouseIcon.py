__author__ = 'newtonis'

import pygame
import source.data.mouse as cursors

cursor = cursors.arrow

def updateCursor():
    global cursor
    cursors.set_cursor(cursor)
    cursor = cursors.arrow
def SetHand():
    global cursor
    cursor = cursors.hand