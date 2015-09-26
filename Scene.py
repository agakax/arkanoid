__author__ = 'Kamil'

from panda3d.core import LPoint3f
from Board import Board
from Paddle import Paddle
from Ball import Ball
from LevelBlocks import LevelBlocks
from GUI import GUI
from DestructibleBlock import DestructibleBlock
from IndestructibleBlock import IndestructibleBlock

collshow = False

class Scene(object):
    __gameEngine = None
    __cameraPosition = LPoint3f(38, -80, 65)
    __cameraDirection = LPoint3f(0, -25, 0)
    __objects = []
    __gui = None
    __gameState = None

    def __init__(self, base, gameEngine, gameState):
        self.__base = base
        self.__gameEngine = gameEngine
        self.setCamera()
        self.__base.taskMgr.add(self.updateTask, "updateTask")
        self.__gameEngine.accept('a', self.switchColliderDisplay)
        self.__gameEngine.accept('r', self.restart)
        self.__gameState = gameState
        self.__gui = GUI(self.__gameEngine, self.__base, self.__gameState)


    def setCamera(self):
        self.__base.disableMouse()
        self.__base.camera.setPos(self.__cameraPosition)
        self.__base.camera.setHpr(self.__cameraDirection)

    def showMenu(self):
        self.__gui.showMenu()
        pass

    def loadGame(self, isPreviousStatePause):
        if not isPreviousStatePause:
            self.destroyObjects()
            self.__objects.append(Board(self.__gameEngine, self.__base))
            self.__objects.append(Paddle(self.__gameEngine, self.__base))
            self.__objects.append(Ball(self.__gameEngine, self.__base))
            self.__objects.append(LevelBlocks(self.__gameEngine, self.__base))
            self.__objects[3].loadLevelBlocks()
            self.drawObjects()

    def pauseGame(self):
        pass

    def destroyObjects(self):
        for obj in self.__objects:
            obj.destroy()
        del self.__objects[:]

    def drawObjects(self):
        for obj in self.__objects:
            obj.draw()

    def updateTask(self, task):
        elapsedTime = self.__gameEngine.getTime()
        self.__gui.update(elapsedTime)
        for obj in self.__objects:
            obj.update(elapsedTime)
        return task.cont

    def switchColliderDisplay(self):
        global collshow
        collshow=not collshow
        if collshow:
            self.__base.cTrav.showCollisions(self.__base.render)
            l=self.__base.render.findAllMatches("**/+CollisionNode")
            for cn in l: cn.show()
        else:
            self.__base.cTrav.hideCollisions()
            l=self.__base.render.findAllMatches("**/+CollisionNode")
            for cn in l: cn.hide()

    def restart(self):
        self.destroyObjects()
        self.loadGame(False)