__author__ = 'ariel'

import pygame
import twisted
import Box2D
from game import *

def main():
    game_handler = Game_handler((900,600),"Testeo bola")

    test1.add_test(game_handler)

    while not game_handler.exit():
        game_handler.update_events()
        game_handler.update()

        game_handler.clear()
        game_handler.draw()
        game_handler.refresh()

if __name__ == "__main__":
    main()