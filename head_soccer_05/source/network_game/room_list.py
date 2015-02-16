__author__ = 'newtonis'

import pygame
from source.network_game.list_system import ListSystem
from source.gui.window import Window
from source.gui.text import Text
from source.data import fonts
from source.gui.button import NeutralButton,AdvancedButton

class RoomList(Window):
    def __init__(self,server_name,room_data,parent):
        self.room_data = room_data
        ww,hh = pygame.display.get_surface().get_size()
        ww -= 50
        hh -= 50
        Window.__init__(self,server_name,(170, 102, 57),(221, 202, 11),0,0,ww,hh,(255,255,255))

        title = Text(fonts.BebasNeue.c40,"GAMES",(255,255,255))
        title.y = 35
        title.x = self.width/2-title.surface.get_size()[0]/2
        self.AddElement(title,"Title")
        listRooms = ListSystem(0,0,False,)
        listRooms.AddUpKey("Name",250)
        listRooms.AddUpKey("Mode",150)
        listRooms.AddUpKey("Stadium",250)
        listRooms.AddUpKey("Players",120)
        listRooms.SetBackground((200,150,150),(50,50,50))
        listRooms.SetUpBackground((41,0,69),(149,0,255))
        listRooms.SetItemColor((23,0,45),(86,0,173))
        listRooms.SetSendInfoDef(self.NewSelected)
        rooms = room_data["info"]
        for x in range(len(rooms)):
            listRooms.AddRow({"Name":rooms[x]["name"],"Mode":rooms[x]["mode"],"Stadium":rooms[x]["stadium"],"Players":str(rooms[x]["players"]["clients"])+"/"+str(rooms[x]["players"]["max-clients"])})

        listRooms.y = 100
        listRooms.x = self.width/2-listRooms.width/2
        self.AddElement(listRooms,"LIST")

        disconnect = NeutralButton("Disconnect",120,(0,0),fonts.BebasNeue.c20)
        disconnect.y = 30
        disconnect.x = 10
        self.AddElement(disconnect,"Disconnect")

        cPlayer = NeutralButton("Change player",120,(0,0),fonts.BebasNeue.c20)
        cPlayer.y = 30
        cPlayer.x = self.width - 10 - cPlayer.imageA.get_size()[0]
        self.AddElement(cPlayer,"cplayer")

        connect = AdvancedButton((350,80),(0,0),"Play",(50,50,200),(50,50,50))
        distance_to_back_list = (listRooms.y + 70 + listRooms.height)
        connect.y = (self.height - distance_to_back_list)/2 + distance_to_back_list - connect.image.get_size()[1]/2
        connect.x = self.width/2 - connect.image.get_size()[0]/2
        self.AddElement(connect,"Connect")

        parent.SetUpdateRoomsDef(self.RoomChanges)
    def ExtraLogicUpdate(self):
        if self.ButtonCheck("Disconnect"):
            self.Kill()
            self.parent.Return2ServerList()
        elif self.ButtonCheck("Connect"):
            self.ConnectTo(self.references["LIST"].selected)
        if self.ButtonCheck("cplayer"):
            self.parent.Go2SelectPlayer()
    def RoomChanges(self,data):
        if data["todo"] == "delete_room":
            self.references["LIST"].DeleteRow(data["key"],data["value"])
        elif data["todo"] == "update_players":
            pass
            #self.references["LIST"]
    def NewSelected(self,selected):
        if selected >= len(self.room_data["info"]):
            return
        clients = self.room_data["info"][selected]["players"]["clients"]
        max_clients = self.room_data["info"][selected]["players"]["max-clients"]
        if clients >= max_clients:
            newtext = "Spectate"
        else:
            newtext = "Play"
        if newtext != self.references["Connect"].text:
            self.references["Connect"].text = "Spectate"
            self.references["Connect"].GenerateButton()
    def ConnectTo(self,room_id):
        name = self.references["LIST"].contents[room_id].content["Name"]
        print "Connect to",name
        self.Send({"action":"join_game","room_name":name})
    def StartJoin(self,data):
        print "Starting to join ..."
        self.parent.SetPitchStart()
    def Send(self,data):
        self.parent.Send(data)