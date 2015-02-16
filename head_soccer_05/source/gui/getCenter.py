__author__ = 'ariel'

def GetCenter(surfaceA,surfaceB):
    wSurfaceA , hSurfaceA = surfaceA.get_size()
    wSurfaceB , hSurfaceB = surfaceB.get_size()
    return wSurfaceA/2-wSurfaceB/2 , hSurfaceA/2-hSurfaceB/2