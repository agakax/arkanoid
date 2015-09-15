__author__ = 'Kamil'

from panda3d.core import LPoint3f
from pandac.PandaModules import CollisionNode, CollisionBox

class Board(object):
    __gameEngine = None
    __board = None
    __position = LPoint3f(0, 0, 0)
    __scale = LPoint3f(15, 15, 15)
    __collider = None
    __boardCenters = []

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.loadModel()
        self.setModelTexture()
        self.setModelParameters()
        self.setBoardCenters()
        self.createCollider()
        self.__collider.show()

    def loadModel(self):
        self.__board = self.__gameEngine.loadModel('models/board')

    def setModelTexture(self):
        self.__gameEngine.setModelTexture(self.__board, 'textures/limba.jpg')

    def setModelParameters(self):
        self.__board.setPos(self.__position)
        self.__board.setScale(self.__scale)

    def setBoardCenters(self):
        boardSizes = self.__board.getTightBounds()
        floorCenter = boardSizes

    def createCollider(self):
        boardPosMin, boardPosMax = self.__board.getTightBounds()
        boardPosMax = LPoint3f(boardPosMax.getX()/self.__scale.getX(), boardPosMax.getY()/self.__scale.getY(), boardPosMax.getZ()/self.__scale.getZ())
        self.__collider = self.__board.attachNewNode(CollisionNode('boardCNode'))
        # Add collider of the floor
        minPos = LPoint3f(boardPosMin - LPoint3f(.1,.1,.1))
        maxPos = LPoint3f(LPoint3f(minPos + LPoint3f(boardPosMax.getX(), boardPosMax.getY(), .2)) + LPoint3f(.1, .1, .1))
        self.__collider.node().addSolid(CollisionBox(minPos, maxPos))
        # Add collider of the left wall
        minPos = boardPosMin
        maxPos = LPoint3f(minPos + LPoint3f(.2, boardPosMax.getY(), boardPosMax.getZ()))
        self.__collider.node().addSolid(CollisionBox(minPos, maxPos))
        # Add collider of the back wall
        minPos = LPoint3f(maxPos - LPoint3f(.2, .2, boardPosMax.getZ()))
        maxPos = LPoint3f(minPos + LPoint3f(boardPosMax.getX(), .2, boardPosMax.getZ()))
        self.__collider.node().addSolid(CollisionBox(minPos, maxPos))
        # Add collider of the right wall
        minPos = LPoint3f(boardPosMin + LPoint3f(boardPosMax.getX() - .2, 0, 0))
        maxPos = LPoint3f(boardPosMax)
        self.__collider.node().addSolid(CollisionBox(minPos, maxPos))


    def draw(self):
        self.__board.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        pass

    def destroy(self):
        self.__board.stash()
        self.__collider.removeNode()