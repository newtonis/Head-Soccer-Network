__author__ = 'newtonis'
import Box2D

value = 0

class MyContactListener(Box2D.b2ContactListener):
    def BeginContact(self,contact):
        global value
        value+=1

        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body

        if bodyA.userData.type == "Ball" and bodyB.userData.type == "Player":
            bodyA.userData.CollisionCallBack(bodyB.userData)

        if bodyB.userData.type == "Ball" and bodyA.userData.type == "Player":
            bodyB.userData.CollisionCallBack(bodyA.userData)


