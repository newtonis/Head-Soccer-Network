class Log_object:
    def __init__(self):
        self.log = {"low":[],"info":[],"critical":[]}
        self.showLow     = False
        self.showInfo    = False
        self.showCritical = True
    def AddLog(self,info,priority):
        self.log[priority].append(info)
    def AddLow(self,info):
        if self.showLow:
            print "I:",info
        self.AddLog(info,"low")
    def AddInfo(self,info):
        if self.showInfo:
            print "Info:",info
        self.AddLog(info,"info")
    def AddCritical(self,info):
        if self.showCritical:
            print "Important:",info
        self.AddLog(info,"critical")
    def EnableShowLow(self):
        self.showLow = True
        self.EnableShowInfo()
    def EnableShowInfo(Self):
        self.showInfo = True
    def DisablePrint(self):
        self.showLow     = False
        self.showInfo    = False
        self.showCritial = False
