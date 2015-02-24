__author__ = 'newtonis'

import pygame
from server.server import WhiteboardServer
from source.data import config

server = None

def main():
    global server
    print "In order to use the server in INTERNET mode ensure you have opened the port 9999 of your router in both TCP and UDP modes"
    server = WhiteboardServer(localaddr=("localhost",9999))#(raw_input("host (your LOCAL IP address):"),9999))

    clock = pygame.time.Clock()
    while server.play:
        server.LogicUpdate()
        clock.tick(40)
if __name__ == "__main__":
    main()
