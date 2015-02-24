__author__ = 'ariel'
import pygame

############### GraphicManager ###############

########################################################################
#######################     IMPORTS      ###############################
from source.gui.rects import RectManager                         #######
from source.gui.window_system import WindowSystem                 ######
from source.gui.checkExit import CheckExit                         #####
from PodSixNet.Connection import connection, ConnectionListener     ####
from source.network_game.server_list import ServerListWindow         ###
from source.network_game.loading_server import LoadingServerWindow   ###
from source.network_game.disconected import DisconectedWindow        ###
from source.network_game.room_list import RoomList                   ###
from source.network_game.network_area import NetworkArea             ###
from source.network_game.ProfileSettings import ProfileSettings      ###
from PodSixNet.ClientUDP import ClientUDP                           ####
from source.data import config                                     #####
from source.database.session_query import *                       ######
########################################################################
########################################################################

class GraphicManager(ConnectionListener,WindowSystem,RectManager): #we are a connection listener as we handle the networking, and a window system because we also deal with windows
    def __init__(self):
        WindowSystem.__init__(self) #init window system
        RectManager.__init__(self) #init rect manager

        self.stage = None #the stage is none because the match is not being played at start. When we enter a room the None value is changed
        self.mode = "Select server" #the start mode is select server, the client must choose a server
        self.start_pump = False #start_pump must be true if the connection to server is started
        self.noCheckExit = False #not used

        self.serverDataCopy = dict() #not used
        w,h = pygame.display.get_surface().get_size() #not used

        #### UDP ####
        print "Starting UDP client ..."
        self.my_id = -1 #the server will tell me what is my id, because I need to tell the server then this IP as UDP connection is informal and the server only will know my ip
        self.UDPconnection = ClientUDP('',9999) #starting the udp bind, in port 9999. UDP don't need to connect to send data, you are free
        self.UDPconnection.SetTarget(self) #we tell udp connection to call my functions when there is new data
        self.UDPconnection.SetPing(config.ping_client) #set the ping simulator (used in debug mode, in play mode is 0)
        self.UDPconnection.SetIrregular(config.irregular_ping) #set the ping simulator irregularity


        #### DEFAULT NETWORK ####
        self.stageActionDef = None #the function that will be called from the game when there is new network data. As in the start there is
        #no stage, the default value is None
    def LogicUpdate(self):
        if self.start_pump: #if we are connected
            self.Pump() #podsixnet library working
            connection.Pump() #podsixnet library working
        #if not self.locked: #if we are allowed to move windows
        #    self.HandleWindows() #handle windows movement
        self.HandleWindows()
        if self.stage: #if we have a stage (where the game is played
            self.stage.LogicUpdate() #update the stage
    def GraphicUpdate(self,screen): #paint the game in the screen
        if self.stage: #if we have a stage
            self.stage.GraphicUpdate(screen) #paint it in the screen
        for window in self.windows: #for each window
            window.GraphicUpdate(screen) #paint it in the screen
        w,h = pygame.display.get_surface().get_size() # not used
        self.AddUpdateRect(0,0,900,600)
        self.ScreenBlit()
    ##### MODES #####
    def StartNetworkGame(self): #if we are ready to display the server list
        self.focused = -1
        self.locked = False
        self.AddWindowCentered(ServerListWindow(),None,"Server List") #add the server list window
    def DecideToPlay(self,room_name): #called when we connect to a server and we want to request rooms
        self.server_name = room_name
        self.mode = "LoadingRoomList" #change our mode to loading
        self.DeleteAllWindows()
        self.Send({"action":"request_rooms"}) #request server the rooms
        self.AddWindowCenteredOnFront(LoadingServerWindow(room_name,self),None,"Loading") #display loading window
    def Return2ServerList(self): #if we disconnect from the game
        self.mode = "Select server" #return to select server status
        self.DeleteAllWindows()
        if self.start_pump:
            self.CloseNetwork() #close network
        self.StartNetworkGame() #start network game again (and open server list window)
    def Go2GameList(self,server_name,data): #if we want to go to a single server game list (it means we are already connected to a server)
        print "Setting game list"
        self.DeleteAllWindows()
        self.mode = "Room List" #change mode to room list mode
        self.AddWindowCenteredOnFront(RoomList(server_name,data,self)) #add room list window
    def Go2SelectPlayer(self):
        self.mode = "Select Player" #change our mode to config player profile mode
        self.DeleteAllWindows()
        self.AddWindowCenteredOnFront(ProfileSettings(self)) #open profile player window
    def RequestsRoomsAgain(self):
        self.Send({"action":"request_rooms"}) #request rooms to server
    def StartGame(self,data): #called when the game is ready to start (you have joined a room successfully)
        print "Starting game"

        self.DeleteAllWindows()
        self.mode = "Playing"
        self.stage = NetworkArea(data,self) #add the stage with the initial data and myself
    def ReturnRoomListFP(self): #if we want to return from profile to room list
        ### FROM PROFILE ###
        print "Going from profile to room list"
        self.DeleteAllWindows()
        self.RequestsRoomsAgain() #request rooms
        self.AddWindowCenteredOnFront(LoadingServerWindow(self.server_name,self,True)) #add the loading window while we wait for the rooms
    def ReturnRoomList(self): #if we want to go from the stage game to room list
        ### FROM GAME ###
        print "Exiting game, going to room list"
        self.Send({"action":"exit_game"}) #send the server that information
        self.RequestsRoomsAgain() #request server the rooms
        self.stage = None #delete the stage. We don't need it anymore
        self.AddWindowCenteredOnFront(LoadingServerWindow(self.server_name,self,True)) #add the loading window while we wait for the rooms
    def OpenCheckExit(self): #add the warning before exiting
        self.noCheckExit = True
        self.AddWindowCenteredOnFront(CheckExit()) #add that window
    ##### GAME RESULTS #####
    def JoinA(self):
        self.Send({"action":"joinA"}) #if we want to join the 'A' side
    def JoinB(self):
        self.Send({"action":"joinB"}) #if we want to join the 'B' side
    def Spectate(self):
        self.Send({"action":"spectate"}) #if we want to join as spectator
    ##### NETWORK #####
    def TryConnection(self,host,port): #call to attempt a connection to a server
        print "Trying to connect to ",host,":",port
        self.Connect((host,port))
        self.host = host
        self.port = port
        self.UDPconnection.SetHost(self.host) #set udp host to that value (to send the data)
        self.start_pump = True #set network variable to true
    def Network_connected(self,data): #called when a tryConnection is successful
        print "connected!"
        self.connectDef(data) #call our connect function that handles what happends when we are connected
    def Network_error(self,data): #called when a tryConnection fail
        print "error ",data["error"]
        self.networkErrorDef(data["error"]) #call our error function that handles what happends when there is an error
        connection.Close() #close connection
    def Network_basic_data(self,data): #called when server send to us the basic data of the game (the players amount, if he accept us and our id)
        self.my_id = data["id"] #our id is needed for the udp, as we need it to identify us in the server as udp is not authenticated
        self.rbasicDef(data) #call our function to handle the basic data
    def Network_udp_signal(self,data): #called when server send us the udp ping signal (used to calculate the ping and show in screen)
        self.udpSignalDef()  #call our function that handle the udp signal
    def Network_disconnected(self,data): #called when the server disconnect us (our connection is lost or the server crashed
        print "Network connection lost"

        if self.mode != "Select server": #if the mode is not the first mode
            self.stage = None #delete stage if we are playing
            self.Return2ServerList() #return to server list (in order to let the player connect to another server)
            self.AddWindowCenteredOnFront(DisconectedWindow(),None,"Error") #add the disconnected message
    def Network_opinion(self,data): #called when the server request us to fill a survey
        self.optionRoomsDef("opinion",data) #our function that handles that
    def Network_rooms_data(self,data): #called  when the server send us data of the rooms
        self.optionRoomsDef("rooms",data) #our function that handles that
    def Network_skip_opinion(self,data): #called when server let us to skip the survey
        self.optionRoomsDef("skip",data) #our function that handles that
    def Network_request_name(self,data): #called when server request us to send our name
        self.optionRoomsDef("req-name",data) #our function that handles that
    def Network_update_rooms(self,data): #called when the server send us information of the rooms
        self.updateRoomsDef(data) #our function that handles that
    def Network_initial_join(self,data): #called when the server send us initial information when we have just joined
        self.my_id = data["id"] #we set our id
        self.StartGame(data) #call our start game function to handle that
    def Network_data_players(self,data): #
        self.playersDef(data)
    def Network_name_error(self,data): #called when the server tells us there is an error with the name we have just sent
        self.optionRoomsDef("error-name",data) #call the function that handles that
    def Network_sa(self,data): #all stage messages that the server sends are redirected to the same function
        if self.stageActionDef: #if the function is defined
            self.stageActionDef(data) #handle the data
    def Network_profile_conf_error(self,data): #called when the server tell us that there is an error with the profile configuration
        self.profileSettingsDef(data) #the function that handles that
    def Network_confirm_login(self,data):
        self.loginDef(data)
    #### UDP ####
    def Network_UDP_data(self,data): #called when there is new udp data (called from UDPconnection)
        connection.Network(data) #tell the connection to handle that information
    def SendUDP(self,data): #called when we want to send udp data
        if self.my_id == -1: #if we don't have our id we can not send data as the server can not identify who we are
            print "Can't send UDP data because id=-1"
            return

        self.UDPconnection.Send(data,self.my_id) #send the data
    #### SETTING NETWORK DEF ####
    def SetErrorDef(self,func):  ##All this functions are equal and are to set the functions that will operate when there is server data ##
        self.networkErrorDef = func
    def SetConnectDef(self,func):
        self.connectDef = func
    def SetOptionRoomsDef(self,func):
        self.optionRoomsDef = func
    def SetRBasicDef(self,func):
        self.rbasicDef = func
    def SetUDPsignalDef(self,func):
        self.udpSignalDef = func
    def SetUpdateRoomsDef(self,func):
        self.updateRoomsDef = func
    def SetPlayersDef(self,func):
        self.playersDef = func
    def SetStageActionDef(self,func):
        self.stageActionDef = func
    def SetProfileSettingsDef(self,func):
        self.profileSettingsDef = func
    def SetLoginDef(self,func):
        self.loginDef = func
    def Network(self,data):
        if data["action"] == "rooms_data":
            print "Rooms data received"
        elif data["action"] == "initial_join":
            print "Join data received"
        elif data["action"] == "sa":
            pass
        else:
            print data
    def CloseNetwork(self): #called when we want to close network
        print "Disconnected from server"
        self.start_pump = False
        connection.Close()
    def End(self): #called to close UDP Connection
        if self.UDPconnection:
            self.UDPconnection.End()

