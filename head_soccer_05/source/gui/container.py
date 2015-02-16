__author__ = 'newtonis'

class Container:
    def __init__(self):
        self.Ereferences = dict()
        self.Eelements = []
        self.x = 0
        self.y = 0
    def LogicUpdate(self):
        for element in self.Eelements:
            element.LogicUpdate()
    def GraphicUpdate(self,screen):
        for element in self.Eelements:
            element.GraphicUpdate(screen)
    def Add(self,element,reference = "NoReference"):
        element.enabled = True
        element.parent = self
        self.Eelements.append(element)
        if reference != "NoReference":
            self.Ereferences[reference] = element
    def Delete(self,id):
        if not self.Ereferences.has_key(id):
            return
        for ex in range(len(self.Eelements)):
            if self.Eelements[ex] == self.Ereferences[id]:
                del self.Eelements[ex]
                del self.Ereferences[id]
                return
    def ButtonCheck(self,id):
        if self.Ereferences.has_key(id):
            if self.Ereferences[id].pressed:
                return True
        return False