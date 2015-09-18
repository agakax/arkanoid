__author__ = 'Kamil'

from panda3d.core import LPoint3f
from Board import Board
from Paddle import Paddle
from Ball import Ball
from LevelBlocks import LevelBlocks
from DestructibleBlock import DestructibleBlock
from IndestructibleBlock import IndestructibleBlock

collshow = False

class Scene(object):
    __gameEngine = None
    __cameraPosition = LPoint3f(38, -80, 65)
    __cameraDirection = LPoint3f(0, -25, 0)
    __objects = []

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.setCamera()
        self.__gameEngine.taskMgr.add(self.updateTask, "updateTask")
        self.__gameEngine.accept('a', self.switchColliderDisplay)
        #self.__gameEngine.accept('d', self.hit)
        self.__gameEngine.accept('r', self.restart)

    def setCamera(self):
        self.__gameEngine.disableMouse()
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
            self.__objects.append(LevelBlocks(self.__gameEngine))
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
        for obj in self.__objects:
            obj.update(elapsedTime)
        return task.cont

    def switchColliderDisplay(self):
        global collshow
        collshow=not collshow
        if collshow:
            self.__gameEngine.cTrav.showCollisions(self.__gameEngine.render)
            l=self.__gameEngine.render.findAllMatches("**/+CollisionNode")
            for cn in l: cn.show()
        else:
            self.__gameEngine.cTrav.hideCollisions()
            l=self.__gameEngine.render.findAllMatches("**/+CollisionNode")
            for cn in l: cn.hide()

    #def hit(self):
        #durability = self.__objects[3].ballHit()
        #if durability == 0:
           # self.__objects.remove(self.__objects[3])

    def restart(self):
        self.destroyObjects()
        self.loadGame(False)