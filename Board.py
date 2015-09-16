__author__ = 'Kamil'

from panda3d.core import LPoint3f, LVector3f
from pandac.PandaModules import CollisionNode, CollisionBox
from MathFunctions import *

class Board(object):
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
        self.__board = self.__gameEngine.loadModel('models/board')

    def setModelTexture(self):
        self.__gameEngine.setModelTexture(self.__board, 'textures/limba.jpg')

    def setModelParameters(self):
        self.__board.setPos(self.__position)
        self.__board.setScale(self.__scale)

    def createWallCollider(self):
        self.__colliderWalls = self.__board.attachNewNode(CollisionNode('boardWallsCNode'))
        minPos, maxPos = self.getSurfaceExtremePos('lWall')
        self.__colliderWalls.node().addSolid(CollisionBox(minPos, maxPos))
        minPos, maxPos = self.getSurfaceExtremePos('rWall')
        self.__colliderWalls.node().addSolid(CollisionBox(minPos, maxPos))
        minPos, maxPos = self.getSurfaceExtremePos('bWall')
        self.__colliderWalls.node().addSolid(CollisionBox(minPos, maxPos))

    def createFloorCollider(self):
        self.__colliderFloor = self.__board.attachNewNode(CollisionNode('boardFloorCNode'))
        minPos, maxPos = self.getSurfaceExtremePos('floor')
        self.__colliderFloor.node().addSolid(CollisionBox(minPos, maxPos))

    def getSurfaceExtremePos(self, surface):
        boardMinPos, boardMaxPos = self.__board.getTightBounds()
        boardMaxPos = LPoint3f(divideVectorsElements(boardMaxPos, self.__scale))
        if surface == 'floor':
            minPos = boardMinPos
            maxPos = LPoint3f(multiplyVectorsElements(boardMaxPos, LVector3f(1, 1, 0.15)))
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
        self.__board.stash()
        self.__colliderWalls.removeNode()