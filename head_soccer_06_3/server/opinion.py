__author__ = 'newtonis'

class Question:
    def __init__(self,question):
        self.question = question
        self.options = []
        self.id = 0
    def SetId(self,id):
        self.id = id
    def AddOption(self,option):
        self.options.append(option)
    def GetText(self):
        return {"question":self.question,"options":self.options,"id":self.id}

QuestionOne = Question("What thing should we do first with the game?")
QuestionOne.AddOption("Improve gaming syncronization")
QuestionOne.AddOption("Add Tournaments")
QuestionOne.AddOption("Add 2vs2 Matches")
QuestionOne.AddOption("Add more characters")
QuestionOne.AddOption("Improve graphics")
QuestionOne.AddOption("I don't care!")
QuestionOne.SetId(1)

def Random():
    return QuestionOne.GetText()