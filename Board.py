__author__ = 'Kamil'

from panda3d.core import LPoint3f, LVector3f, BitMask32
from pandac.PandaModules import CollisionNode, CollisionBox, CollisionPlane, Plane
from MathFunctions import *

class Board(object):
    FLOOR_MASK = BitMask32.bit(1)
    WALL_MASK = BitMask32.bit(2)
    __gameEngine = None
    __board = None
    __position = LPoint3f(0, 0, 0)
    __scale = LPoint3f(15, 15, 15)
    __colliderWalls = None
    __colliderFloor = None

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
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
        self.__board.setScale(self.__scale)
        self.__board.setCollideMask(BitMask32.allOff())

    def createWallCollider(self):
        self.__colliderWalls = self.__board.attachNewNode(CollisionNode('boardWallsCNode'))
        minPos, maxPos = self.getSurfaceExtremePos('lWall')
        self.__colliderWalls.node().addSolid(CollisionBox(minPos, maxPos))
        minPos, maxPos = self.getSurfaceExtremePos('rWall')
        self.__colliderWalls.node().addSolid(CollisionBox(minPos, maxPos))
        minPos, maxPos = self.getSurfaceExtremePos('bWall')
        self.__colliderWalls.node().addSolid(CollisionBox(minPos, maxPos))
        self.__colliderWalls.node().setIntoCollideMask(self.WALL_MASK)
        self.__colliderWalls.node().setFromCollideMask(BitMask32.allOff())

    def createFloorCollider(self):
        self.__colliderFloor = self.__board.find("**/floor_collider")
        self.__colliderFloor.node().setIntoCollideMask(self.FLOOR_MASK)
        self.__colliderFloor.node().setFromCollideMask(BitMask32.allOff())

    def getSurfaceExtremePos(self, surface):
        boardMinPos, boardMaxPos = self.__board.getTightBounds()
        boardMaxPos = LPoint3f(divideVectorsElements(boardMaxPos, self.__scale))
        if surface == 'floor':
            minPos = LPoint3f(boardMinPos + multiplyVectorsElements(boardMaxPos, LVector3f(0, 0, 0.265)))
            maxPos = LPoint3f(multiplyVectorsElements(boardMaxPos, LVector3f(1, 1, 0.265)))
            return minPos, maxPos
        elif surface == 'lWall':
            minPos = boardMinPos
            maxPos = LPoint3f(multiplyVectorsElements(boardMaxPos, LVector3f(0.04, 1, 1)))
            return minPos, maxPos
        elif surface == 'rWall':
            minPos = LPoint3f(boardMinPos + multiplyVectorsElements(boardMaxPos, LVector3f(0.96, 0, 0)))
            maxPos = boardMaxPos
            return minPos, maxPos
        elif surface == 'bWall':
            minPos = LPoint3f(boardMinPos + multiplyVectorsElements(boardMaxPos, LVector3f(0, 0.96, 0)))
            maxPos = boardMaxPos
            return minPos, maxPos

    def draw(self):
        self.__board.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        pass

    def destroy(self):
        self.__board.removeNode()
        #self.__colliderWalls.removeNode()