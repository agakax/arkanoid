__author__ = 'Kamil'

from Scene import Scene
import time, sys
from pandac.PandaModules import CollisionTraverser, CollisionHandlerEvent

class EnumGameStates(object):
    EXITING = 0
    INITIALIZING = 1
    MENU = 2
    PLAY = 3
    PAUSE = 4

class GameState(object):
    __gameState = EnumGameStates.INITIALIZING
    __gameScene = None
    __gameEngine = None

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.createGameScene()
        self.setGameState(EnumGameStates.PLAY)
        self.setGameState(EnumGameStates.MENU)
        time.sleep(2)
        self.setGameState(EnumGameStates.PLAY)

    def createGameScene(self):
        self.__gameScene = Scene(self.__gameEngine)

    def setGameState(self, newGameState):
        if self.__gameState != newGameState:
            if newGameState == EnumGameStates.MENU:
                self.__gameScene.loadMenu()
            elif newGameState == EnumGameStates.PLAY:
                isPreviousStatePause = self.__gameState == EnumGameStates.PAUSE
                self.__gameScene.loadGame(isPreviousStatePause)
            elif newGameState == EnumGameStates.PAUSE:
                self.__gameScene.pauseGame()
            elif newGameState == EnumGameStates.EXITING:
                sys.exit()
            self.__gameState = newGameState





