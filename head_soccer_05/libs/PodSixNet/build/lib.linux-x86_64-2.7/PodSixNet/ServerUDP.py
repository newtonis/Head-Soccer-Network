__author__ = 'newtonis'

import socket
import sys
import threading

from async import poll, asyncore
from Channel import Channel
from rencode import loads, dumps

class ServerUDP(asyncore.dispatcher):
    def __init__(self, localaddr=("127.0.0.1", 31425)):
        print "UDP server starting... with ",localaddr
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.bind(localaddr)
        self.target = None
        self.loop_thread = threading.Thread(target=asyncore.loop, name="Asyncore Loop")
        self.loop_thread.start()
    def SetTarget(self,target):
        self.target = target
    def handle_connect(self):
        print "UDP server started ..."
    def handle_read(self):
        data,addr = self.recvfrom(2048)
        if self.target != None:
            self.target.Network_UDP_data(loads(data),addr)
    def handle_write(self):
        pass
    def Send(self , data , addr):
        self.sendto(dumps(data),addr)
    def End(self):
        self.close()

def main():
    serverUDP = ServerUDP("localhost",9999)
    asyncore.loop()
if __name__ == "__main__":
    main()
