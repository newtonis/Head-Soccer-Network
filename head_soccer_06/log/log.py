__author__ = 'grandt'
import pygame
from log_engine import Engine

def main():
    screen = pygame.display.set_mode((900,600),pygame.HWSURFACE)
    pygame.display.set_caption("Logs")
    clock = pygame.time.Clock()
    eng = Engine()
    continuar = True
    while continuar:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                continuar = False
        screen.fill((100,100,100))
        clock.tick(20)
        eng.GraphicUpdate(screen)
        eng.LogicUpdate()
        pygame.display.update()

main()