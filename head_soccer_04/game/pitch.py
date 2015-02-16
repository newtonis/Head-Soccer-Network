__author__ = 'ariel'



def add_server_pitch( handler ):

    handler.add_element( Element( handler.world.CreateStaticBody( position=(0,0),shapes=polygonShape(box=(50,1)),color=(0,0,0) ), handler , base ) )

    handler.add_element( Element(handler.world.CreateStaticBody(position=(0,29.9) ,shapes=polygonShape(box=(50,0.1)),color=(0,0,0) ), handler ,goal) )

    e=handler.add_element(Element(handler.world.CreateDynamicBody(position=(38,2) , linearVelocity=(-randrange(1000),randrange(240)) , bullet=True ), handler  , ball))

    circle=e.body.CreateCircleFixture(radius=0.475, density=200, friction=0.1 ,restitution=0.95)
    handler.ball = circle

    handler.add_element(Head((1,1),images.HeadsImages.headA , handler , False))
    handler.add_element(Head((30,1),images.HeadsImages.headB , handler ))
    goals = Goals(0,handler)
    handler.add_element(goals)
    handler.goal = goals
