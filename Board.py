__author__ = 'Kamil'

from panda3d.core import LPoint3f

class Board(object):
    __gameEngine = None
    __cameraPosition = None
    __cameraDirection = None
    __environPosition = None
    __environScale = None

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.initValues()

        self.setTheCamera()
        self.loadModel()
        self.setModelTexture()
        self.setModelParameters()

    def initValues(self):
        self.__cameraPosition = LPoint3f(25, -45, 40)
        self.__cameraDirection = LPoint3f(0, -25, 0)
        self.__environPosition = LPoint3f(0, 0, 0)
        self.__environScale = LPoint3f(10, 10, 10)

    def setTheCamera(self):
        self.__gameEngine.disableMouse()
        self.__gameEngine.camera.setPos(self.__cameraPosition)
        self.__gameEngine.camera.setHpr(self.__cameraDirection)

    def loadModel(self):
        self.__environ = self.__gameEngine.loader.loadModel("models/board")

    def setModelTexture(self):
        boardTexture = self.__gameEngine.loader.loadTexture('textures/limba.jpg')
        self.__environ.setTexture(boardTexture, 1)

    def setModelParameters(self):
        self.__environ.setScale(self.__environScale)
        self.__environ.setPos(self.__environPosition)

    def draw(self):
        self.__environ.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        pass
