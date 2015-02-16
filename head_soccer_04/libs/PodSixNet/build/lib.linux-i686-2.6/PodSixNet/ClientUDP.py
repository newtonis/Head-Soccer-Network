__author__ = 'newtonis'
import socket, asyncore
from rencode import loads, dumps

class ClientUDP(asyncore.dispatcher):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.buffer = ""
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.bind( ('', 0) )
    def handle_connect(self):
        print "UDP client connected!"
    def handle_close(self):
        print "Client closed"
        self.close()
    def handle_read(self):
        data ,addr = self.recvfrom(2048)

        print loads(data)
        #print "Data received: ",data

    def handle_write(self):
        if self.buffer != "":
            sent = self.sendto(self.buffer,(self.host,self.port))
            self.buffer = self.buffer[sent:]
    def Send(self, data):
        self.sendto(dumps(data),(self.host,self.port))
def main():
    clientUDP = ClientUDP("localhost",9999)

    clientUDP.Send({"pack":"lololol","more":"dgaseg"})
    while 1:
        asyncore.loop(count=50)
        #data = raw_input("chat >")
        #clientUDP.Send(data)
if __name__ == "__main__":
    main()