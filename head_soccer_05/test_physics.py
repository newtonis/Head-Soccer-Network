__author__ = 'newtonis'
import pygame
from server.stadiums import *
from source.physics.game import *
from source.physics.gameV2 import *

def main():
    screen = pygame.display.set_mode((900,600))
    game   = PowerGameEngine("server")
    game.AddPitch("classic")
    game.AddBall((20,0.5),(0,4),(0,0,0),0)
    game.AddPlayer("head A","A1",1)
    game.AddPlayer("head C","A2",2)
    game.elements["0"].SetMask(LAYER_1,LAYER_1)
    game.elements["1"].SetMask(LAYER_1,LAYER_1)
    game.elements["2"].SetMask(LAYER_1,LAYER_1)
    print game.GetDynamicCodes()
    clock = pygame.time.Clock()
    continuar = True
    while continuar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuar = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    continuar = False
                if event.key == pygame.K_SPACE:
                    game.GoalEffectA()
                if event.key == pygame.K_r:
                    main()
                    continuar = False
        keys = pygame.key.get_pressed()
        screen.fill((200,200,255))
        game.GraphicUpdate(screen)
        game.LogicUpdate()
        game.HandlePlayerActions("A1",get_key_actions(keys))
        #if game.elements[0].position[0] > game.elements[2].position[0]:
        #    keys[pygame.K_a] = True
        game.HandlePlayerActions("A2",get_alternative_key_actions(keys))
        pygame.display.flip()
        clock.tick(40)

if __name__ == "__main__":
    main()