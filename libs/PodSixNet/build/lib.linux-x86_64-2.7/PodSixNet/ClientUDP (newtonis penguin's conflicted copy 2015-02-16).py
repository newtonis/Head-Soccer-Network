__author__ = 'newtonis'
import socket, asyncore
from rencode import loads, dumps
import threading
import time
import random

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
        self.pingAdded = 0
        self.sid = 0
        self.irregularPercentaje = 0
        self.calculatePingSignal = False
    def StartCalculatePing(self):
        self.calcuatePingSignal = True
    def SetIrregular(self,percentaje):
        self.irregularPercentaje = percentaje
    def SetPing(self,ping):
        self.pingAdded = ping
    def SetHost(self,host):
        print "Setting host to",host
        self.host = host
    def SetTarget(self,target):
        self.target = target
    def handle_connect(self):
        print "UDP client connected!"
    def handle_close(self):
        print "Client closed"
        self.close()
    def handle_read(self):
        data ,addr = self.recvfrom(2048)
        if self.target:
            self.target.Network_UDP_data(loads(data))
    def handle_write(self):
        if self.buffer != "":
            sent = self.sendto(self.buffer,(self.host,self.port))
            self.buffer = self.buffer[sent:]
    def Send(self, data,id):
        #print "UDP data sent!:",data,"as",id
        self.refTime = time.time()
        if self.pingAdded != 0:
            self.sid += 1
            th_send = threading.Thread(target=self.ThSend,name="Send th"+str(self.sid),args=(data,id))
            th_send.start()
        else:
            self.sendto(dumps({"content":dumps(data),"id":id}),(self.host,self.port))
    def ThSend(self,data,id):
        #print float(self.pingAdded)/1000.0
        percentaje = float(self.pingAdded) * float(self.irregularPercentaje) / 100.0
        min_percentaje = -percentaje
        max_percentaje = +percentaje
        ping_error = random.uniform(min_percentaje,max_percentaje)
        final_ping = self.pingAdded + ping_error

        time.sleep(float(final_ping)/1000.0)
        self.sendto(dumps({"content":dumps(data),"id":id}),(self.host,self.port))

    def End(self):
        print "UDP client closed"
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