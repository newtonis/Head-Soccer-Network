__author__ = 'newtonis'
import pygame
from source.gui.input import Input
from source.gui.element import Element

### ARCHIVO PARA PROBAR COSAS POR SEPARADO ###

class Screen(Element):
    def __init__(self):
        self.x = 0
        self.y = 0

def main():
    screen = pygame.display.set_mode((800,600))

    test_elements = []
    inp = Input()
    inp.AllowAll()
    inp.x = 400
    inp.y = 400
    inp.parent = Screen()
    test_elements.append(inp)
    continuar = True
    while continuar:
        events = pygame.event.get()
        for element in test_elements:
            element.Event(events)
        for event in events:
            if event.type == pygame.QUIT:
                continuar = False
        screen.fill((255,255,255))
        for element in test_elements:
            element.LogicUpdate()
            element.GraphicUpdate(screen)

        pygame.display.update()

if __name__ == "__main__":
    main()