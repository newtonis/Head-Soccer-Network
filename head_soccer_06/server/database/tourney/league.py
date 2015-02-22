__author__ = 'newtonis'

from tourney import Tournament

class League(Tournament):
    def __init__(self):
        Tournament.__init__(self)
        self.SetName("classic 4 team league")
        self.AddDescriptionLine("This is a simple competition, each team")
        self.AddDescriptionLine("plays 3 matches, totaling 6 tournament")
        self.AddDescriptionLine("matches, always playing 2 at the same time")
        self.AddDescriptionLine("Each victory gives 3 points while each draw gives 1")
        self.AddDescriptionLine("The winner is defined by points then GD, then GS")

        self.SetType("4 team league")