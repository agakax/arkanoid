__author__ = 'Kamil'

from GameState import *

class GameSaver(object):
    __gameState = None

    def __init__(self, gameState):
        self.__gameState = gameState

    def saveState(self):
        # Save points/current level/lives etc.
        pass