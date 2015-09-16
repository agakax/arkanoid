__author__ = 'Kamil'

from pandac.PandaModules import LPoint3f, LVector3f

def multiplyVectorsElements(vec1, vec2):
    return LVector3f(vec1.getX()*vec2.getX(), vec1.getY()*vec2.getY(), vec1.getZ()*vec2.getZ())

def divideVectorsElements(vec1, vec2):
    if vec2.getX() == 0 or vec2.getY() == 0 or vec2.getZ() == 0:
        return LVector3f(vec1)
    return LVector3f(vec1.getX()/vec2.getX(), vec1.getY()/vec2.getY(), vec1.getZ()/vec2.getZ())