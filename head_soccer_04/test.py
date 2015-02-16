import pygame
from images import list_server_images


def main():
    screen  = pygame.display.set_mode((800,400))
    play    = True 
    surface = list_server_images.GetBlueItem(600)
    while play:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        screen.blit(surface,(0,0))
        pygame.display.update()
 

if __name__ == "__main__":
    main()
