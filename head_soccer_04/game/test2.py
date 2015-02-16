__author__ = 'ariel'

import pygame
import twisted
import Box2D
from Box2D.b2 import *

def add_test(handler):
    ground = handler.world.CreateStaticBody(
    position=(0,0),
    shapes=b2EdgeShape(vertices=[(-20,0), (20,0)])
    )

    # Collinear edges
    handler.world.CreateStaticBody(
                    shapes=[b2EdgeShape(vertices=[(-8,1), (-6,1)]),
                            b2EdgeShape(vertices=[(-6,1), (-4,1)]),
                            b2EdgeShape(vertices=[(-4,1), (-2,1)]),
                            ]
                )

    # Square tiles
    handler.world.CreateStaticBody(
                    shapes=[b2PolygonShape(box=[1, 1, (4,3), 0]),
                            b2PolygonShape(box=[1, 1, (6,3), 0]),
                            b2PolygonShape(box=[1, 1, (8,3), 0]),
                            ]
                )

    # Square made from an edge loop. Collision should be smooth.
    body=handler.world.CreateStaticBody()
    body.CreateLoopFixture(vertices=[(-1,3), (1,3), (1,5), (-1,5)])

    # Edge loop.
    body=handler.world.CreateStaticBody(position=(-10,4))
    body.CreateLoopFixture(vertices=[
                        (0.0, 0.0), (6.0, 0.0),
                        (6.0, 2.0), (4.0, 1.0),
                        (2.0, 2.0), (0.0, 2.0),
                        (-2.0,2.0), (-4.0,3.0),
                        (-6.0,2.0), (-6.0,0.0),]
                        )

    # Square character 1
    handler.world.CreateDynamicBody(
                    position=(-3, 8),
                    fixedRotation=True,
                    allowSleep=False,
                    fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 0.5)), density=20.0),
                )

    # Square character 2
    body=handler.world.CreateDynamicBody(
                    position=(-5, 5),
                    fixedRotation=True,
                    allowSleep=False,
                )

    body.CreatePolygonFixture(box=(0.25, 0.25), density=20.0)

    # Hexagon character
    a=b2_pi/3.0
    handler.world.CreateDynamicBody(
                    position=(-5, 8),
                    fixedRotation=True,
                    allowSleep=False,
                    fixtures=b2FixtureDef(
                            shape=b2PolygonShape(vertices=[(0.5*cos(i*a), 0.5*sin(i*a)) for i in range(6)]),
                            density=20.0
                            ),
                )

    # Circle character
    handler.world.CreateDynamicBody(
                    position=(3, 5),
                    fixedRotation=True,
                    allowSleep=False,
                    fixtures=b2FixtureDef(
                            shape=b2CircleShape(radius=0.5),
                            density=20.0
                            ),
                )