__author__ = 'Kamil'

from panda3d.core import LPoint3f
from pandac.PandaModules import CollisionNode, CollisionBox

class Board(object):
    __gameEngine = None
    __board = None
    __position = LPoint3f(0, 0, 0)
    __scale = LPoint3f(15, 15, 15)

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.loadModel()
        self.setModelTexture()
        self.setModelParameters()

        self.__collider.show()

    def loadModel(self):
        self.__board = self.__gameEngine.loadModel('models/board')

    def setModelTexture(self):
        self.__gameEngine.setModelTexture(self.__board, 'textures/limba.jpg')

    def setModelParameters(self):
        self.__board.setPos(self.__position)
        self.__board.setScale(self.__scale)

    def draw(self):
        self.__board.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        pass

    def destroy(self):
        self.__board.destroy()