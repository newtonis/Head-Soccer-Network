import pygame

def load_route(file):
    return pygame.image.load("images/"+file)

class ServerItems:
     class Blue:
         Left   = load_route("server_item_blue/left.png")
         Center = load_route("server_item_blue/center.png")
         Right  = load_route("server_item_blue/right.png")

def GetBlueItem(width):
    surface = pygame.surface.Surface((width,50),pygame.SRCALPHA)
    surface.blit(ServerItems.Blue.Left,(0,0))
    surface.blit(ServerItems.Blue.Right,(width-ServerItems.Blue.Right.get_size()[0],0))
    for x in range(ServerItems.Blue.Left.get_size()[0],width-ServerItems.Blue.Right.get_size()[0]):
         surface.blit(ServerItems.Blue.Center,(x,0))
    return surface
