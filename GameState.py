__author__ = 'Kamil'

from Scene import Scene
import time, sys
from EnumGameStates import EnumGameStates

class GameState(object):
    __state = EnumGameStates.INITIALIZING
    __gameScene = None
    __gameEngine = None
    __base = None
    __gui = None
    def __init__(self, gameEngine, base):
        self.__base = base
        self.__gameEngine = gameEngine
        self.createGameScene()
        self.setGameState(EnumGameStates.MENU)

    def createGameScene(self):
        self.__gameScene = Scene(self.__base, self.__gameEngine, self)

    def getGameState(self):
        return self.__state

    def setGameState(self, newGameState):
        if self.__state != newGameState:
            if newGameState == EnumGameStates.MENU:
                self.__gameScene.showMenu()
            elif newGameState == EnumGameStates.PLAY:
                isPreviousStatePause = self.__state == EnumGameStates.PAUSE
                self.__gameScene.loadGame(isPreviousStatePause)
            elif newGameState == EnumGameStates.PAUSE:
                self.__gameScene.pauseGame()
            elif newGameState == EnumGameStates.EXITING:
                sys.exit()
            self.__state = newGameState





