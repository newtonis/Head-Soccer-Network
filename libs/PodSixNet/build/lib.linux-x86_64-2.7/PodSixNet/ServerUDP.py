__author__ = 'newtonis'

import socket
import sys
import threading

from async import poll, asyncore
from Channel import Channel
from rencode import loads, dumps
import time

class ServerUDP(asyncore.dispatcher):
    def __init__(self, localaddr=("127.0.0.1", 31425)):
        print "UDP server starting... with ",localaddr
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.bind(localaddr)
        self.target = None
        self.loop_thread = threading.Thread(target=AsyncoreThread, name="Asyncore Loop")
        self.loop_thread.start()
        self.pingAdded = 0
        self.sid = 0
    def SetPing(self,ping):
        self.pingAdded = ping
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
        if self.pingAdded == 0:
            self.sendto(dumps(data),addr)
        else:
            self.sid += 1
            th_send = threading.Thread(target=self.ThSend,name="Send th"+str(self.sid),args=(data,addr))
            th_send.start()
    def ThSend(self,data,addr):
        time.sleep(float(self.pingAdded)/1000.0)
        self.sendto(dumps(data),addr)
    def End(self):
        print "UDP server closed "
        self.close()
        asyncore.close_all()

def AsyncoreThread():
    print "Starting asyncore thread"
    asyncore.loop(use_poll=True)
    print "Ending asyncore thread ..."

def main():
    serverUDP = ServerUDP("localhost",9999)

    asyncore.loop()


if __name__ == "__main__":
    main()
