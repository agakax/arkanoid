__author__ = 'Kamila'
#from panda3d.core import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

from direct.showbase.ShowBase import ShowBase
from GameState import GameState

class ArkanoidGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        GameState(self)
app = ArkanoidGame()
app.run()