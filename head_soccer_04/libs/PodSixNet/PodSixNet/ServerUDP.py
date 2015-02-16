__author__ = 'newtonis'

import socket
import sys

from async import poll, asyncore
from Channel import Channel
from rencode import loads, dumps

class ServerUDP(asyncore.dispatcher):
    def __init__(self, host,port):
        self.host = host
        self.port = port
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.bind((host,port))
    def handle_connect(self):
        print "UDP server started ..."
    def handle_read(self):
        data,addr = self.recvfrom(2048)
        print "Data received:",str(addr) + " >> "+ data
        self.sendto(data,addr)
    def handle_write(self):
        pass


def main():
    serverUDP = ServerUDP("localhost",9999)
    asyncore.loop()
if __name__ == "__main__":
    main()
