__author__ = 'newtonis'
import socket, asyncore
from rencode import loads, dumps
import threading

class ClientUDP(asyncore.dispatcher):
    def __init__(self,host,port):
        print "UDP client starting... with ",host,":",port
        self.host = host
        self.port = port
        self.buffer = ""
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.bind( ('', 0) )
        self.target = None
        self.loop_thread = threading.Thread(target=asyncore.loop, name="Asyncore Loop")
        self.loop_thread.start()

    def SetTarget(self,target):
        self.target = target
    def handle_connect(self):
        print "UDP client connected!"
    def handle_close(self):
        print "Client closed"
        self.close()
    def handle_read(self):
        data ,addr = self.recvfrom(2048)
        if self.target != None:
            self.target.Network_UDP_data(loads(data))
    def handle_write(self):
        if self.buffer != "":
            sent = self.sendto(self.buffer,(self.host,self.port))
            self.buffer = self.buffer[sent:]
    def Send(self, data,id):
        #print "UDP data sent!:",data,"as",id
        self.sendto(dumps({"content":dumps(data),"id":id}),(self.host,self.port))
    def End(self):
        self.close()
def main():
    clientUDP = ClientUDP("200.114.235.59",9999)

    clientUDP.Send({"pack":"lololol","more":"dgaseg"})
    while 1:
        asyncore.loop(count=50)
        #data = raw_input("chat >")
        #clientUDP.Send(data)
if __name__ == "__main__":
    main()