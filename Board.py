__author__ = 'Kamil'

from panda3d.core import LPoint3f, LVector3f, BitMask32
from pandac.PandaModules import CollisionNode, CollisionPolygon
from MathFunctions import *

class Board(object):
    FLOOR_MASK = BitMask32.bit(1)
    WALL_MASK = BitMask32.bit(2)
    SCALE = 15
    __gameEngine = None
    __board = None
    __position = None
    __colliderSideWalls = None
    __colliderBackWall = None
    __colliderFloor = None

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.__position = LPoint3f(0, 0, 0)
        self.loadModel()
        self.setModelTexture()
        self.setModelParameters()
        self.createWallCollider()
        self.createFloorCollider()

    def loadModel(self):
        self.__board = self.__gameEngine.loadModel('models/board3')

    def setModelTexture(self):
        self.__gameEngine.setModelTexture(self.__board, 'textures/limba.jpg')

    def setModelParameters(self):
        self.__board.setPos(self.__position)
        self.__board.setScale(self.SCALE)
        self.__board.setCollideMask(BitMask32.allOff())

    def createWallCollider(self):
        self.__colliderSideWalls = self.__board.attachNewNode(CollisionNode('boardSideWallsCNode'))
        point1, point2, point3, point4 = self.getWallVertices('left')
        self.__colliderSideWalls.node().addSolid(CollisionPolygon(point1, point2, point3, point4))
        point1, point2, point3, point4 = self.getWallVertices('right')
        self.__colliderSideWalls.node().addSolid(CollisionPolygon(point1, point2, point3, point4))
        self.__colliderSideWalls.node().setIntoCollideMask(self.WALL_MASK)
        self.__colliderSideWalls.node().setFromCollideMask(BitMask32.allOff())
        self.__colliderBackWall = self.__board.attachNewNode(CollisionNode('boardBackWallCNode'))
        point1, point2, point3, point4 = self.getWallVertices('back')
        self.__colliderBackWall.node().addSolid(CollisionPolygon(point1, point2, point3, point4))
        self.__colliderBackWall.node().setIntoCollideMask(self.WALL_MASK)
        self.__colliderBackWall.node().setFromCollideMask(BitMask32.allOff())


    def createFloorCollider(self):
        self.__colliderFloor = self.__board.find("**/floor_collider")
        self.__colliderFloor.node().setIntoCollideMask(self.FLOOR_MASK)
        self.__colliderFloor.node().setFromCollideMask(BitMask32.allOff())

    def getWallVertices(self, wall):
        boardMinPos, boardMaxPos = self.__board.getTightBounds()
        boardMaxPos = LPoint3f(boardMaxPos/self.SCALE)
        if wall == 'left':
            point1 = LPoint3f(boardMinPos + multiplyVectorsElements(boardMaxPos, LVector3f(0.0027*self.SCALE, 0, 0)))
            point2 = LPoint3f(point1 + multiplyVectorsElements(boardMaxPos, LVector3f(0, 1, 0)))
            point3 = LPoint3f(point2 + multiplyVectorsElements(boardMaxPos, LVector3f(0, 0, 1)))
            point4 = LPoint3f(point1 + multiplyVectorsElements(boardMaxPos, LVector3f(0, 0, 1)))
            return point1, point2, point3, point4
        elif wall == 'right':
            point1 = LPoint3f(boardMinPos + multiplyVectorsElements(boardMaxPos, LVector3f(1 - (0.0027*self.SCALE) ,0 ,0)))
            point2 = LPoint3f(point1 + multiplyVectorsElements(boardMaxPos, LVector3f(0, 0, 1)))
            point3 = LPoint3f(point2 + multiplyVectorsElements(boardMaxPos, LVector3f(0, 1, 0)))
            point4 = LPoint3f(point1 + multiplyVectorsElements(boardMaxPos, LVector3f(0, 1, 0)))
            return point1, point2, point3, point4
        elif wall == 'back':
            point1 = LPoint3f(boardMinPos + multiplyVectorsElements(boardMaxPos, LVector3f(0, 1 - (0.0027*self.SCALE), 0)))
            point2 = LPoint3f(point1 + multiplyVectorsElements(boardMaxPos, LVector3f(0, 0, 1)))
            point3 = LPoint3f(point2 + multiplyVectorsElements(boardMaxPos, LVector3f(1, 0, 0)))
            point4 = LPoint3f(point1 + multiplyVectorsElements(boardMaxPos, LVector3f(1, 0, 0)))
            return point1, point2, point3, point4

    def draw(self):
        self.__board.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        pass

    def destroy(self):
        self.__board.removeNode()