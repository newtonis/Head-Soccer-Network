__author__ = 'newtonis'


class Tournament:
    def __init__(self):
        self.currentMatches = [] #matches currently being played in the tournament
        self.description = []
        self.teams = 0 #team amount required to play the tournament
        self.spectators = dict() #players that see the tournament
        self.playing = dict()
        self.type = ""
        self.name = ""
    def AddDescriptionLine(self,line):
        self.description.append(line)
    def SetType(self,type):
        self.type = type
    def AddSpector(self,client):
        print "Player",client.GetID(),"has joined as spectator"
        self.spectators[client.id] = client
    def SetName(self,name):
        self.name = name
    def PlayerPlay(self,player):
        print "Player",player.GetID(),"has joined torunament '",self.name,"'"
        self.playing[player.id] = player
    def PlayerExitTornament(self,player):
        print "Player",player.GetID,"has abandonend the game"
        del self.playing[player.id]
    def PlayerExitSpectate(self,player):
        print "Player",player.GetID,"is no longer seeing the game"
        del self.spectators[player.id]
    def GetBasicData(self):
         return {"name":self.name,"stadium":self.stadium["name"],"mode":self.type,"playing":len(self.playing),"players":self.GetPlayersData()}
    def GetPlayersData(self):
        return {"play":0,"clients":len(self.playing),"max-clients":self.teams}