__author__ = 'newtonis'

import pygame
from server.server import WhiteboardServer
from log.log_client import Log

server = None

def main():
    global server
    Log.SetBasic("Server",(0,255,209),(0,255,119),0)
    Log.Print("In order to use the server in INTERNET mode ensure you have opened the port 9999 of your router in both TCP and UDP modes")
    server = WhiteboardServer(localaddr=("localhost",9999))#(raw_input("host (your LOCAL IP address):"),9999))

    clock = pygame.time.Clock()
    while server.play:
        try:
            server.LogicUpdate()
            Log.LogicUpdate()
            clock.tick(40)
        except Exception as e:
            Log.PrintError(e)
if __name__ == "__main__":
    main()
