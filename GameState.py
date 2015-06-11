__author__ = 'Kamil'

from time import clock
from Board import Board
from Ball import Ball
from Paddle import Paddle
from pandac.PandaModules import ClockObject

class EnumGameStates(object):
    EXITING = 0
    INITIALIZING = 1
    MENU = 2
    PLAY = 3
    PAUSE = 4

class GameState(object):
    __gameState = EnumGameStates.INITIALIZING
    __objects = []
    __game = None
    __elapsedTime = 0.0
    __clock = ClockObject.getGlobalClock()
    def __init__(self, game):
        self.__game = game
        self.createObjects()
        for obj in self.__objects:
            obj.draw()
        self.__game.taskMgr.add(self.updateTask, "updateTask")

    def createObjects(self):
        board = Board(self.__game)
        self.__objects.append(board)
        ball = Ball(self.__game)
        self.__objects.append(ball)
        paddle = Paddle(self.__game)
        self.__objects.append(paddle)

    def updateTask(self, task):
        self.__elapsedTime = self.__clock.getDt()
        self.__objects[2].update(self.__elapsedTime)
        return task.cont

