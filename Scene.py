__author__ = 'Kamil'

from panda3d.core import LPoint3f
from Board import Board
from Paddle import Paddle
from Ball import Ball

class Scene(object):
    __gameEngine = None
    __cameraPosition = LPoint3f(40, -60, 40)
    __cameraDirection = LPoint3f(0, -25, 0)
    __objects = []

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.setCamera()
        self.__gameEngine.taskMgr.add(self.updateTask, "updateTask")

    def setCamera(self):
        #self.__gameEngine.disableMouse()
        self.__gameEngine.camera.setPos(self.__cameraPosition)
        self.__gameEngine.camera.setHpr(self.__cameraDirection)

    def loadMenu(self):
        #self.destroyObjects()
        #self.drawObjects()
        pass

    def loadGame(self, isPreviousStatePause):
        if not isPreviousStatePause:
            self.destroyObjects()
            self.__objects.append(Board(self.__gameEngine))
            self.__objects.append(Paddle(self.__gameEngine))
            self.__objects.append(Ball(self.__gameEngine))
            self.drawObjects()

    def pauseGame(self):
        pass

    def destroyObjects(self):
        for obj in self.__objects:
            obj.destroy()
        self.__objects = []

    def drawObjects(self):
        for obj in self.__objects:
            obj.draw()

    def updateTask(self, task):
        elapsedTime = self.__gameEngine.getTime()
        for obj in self.__objects:
            obj.update(elapsedTime)
        return task.cont