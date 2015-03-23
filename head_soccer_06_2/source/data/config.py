__author__ = 'newtonis'

from source.database import serverQ

ping_server = 0
ping_client = 0
irregular_ping = 0 #%

local_host = "localhost"
dylan_server_host = "192.168.1.45"
newtonis_server_host = "192.168.1.59"

current_host = dylan_server_host #currently is not being used as there is a raw_input

data = serverQ.GetConfigData()
threshold = data[1] #0.001 #correction in the client, if a target position has less than threshold distance, it is corrected
interpolation_constant = data[0] #0.30 #smooth client movement speed
match_duration = 0.1#3 #the duration of the match in minutes


CLOSE_WHEN_CLIENT_LOST = False #used for debugging propouses