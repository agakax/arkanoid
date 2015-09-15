__author__ = 'Kamila'
#from panda3d.core import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject, CollisionHandlerEvent, CollisionTraverser
from GameState import GameState

class ArkanoidGame(ShowBase):
    __clock = ClockObject.getGlobalClock()
    __collisionHandler = CollisionHandlerEvent()
    __gameState = None
    def __init__(self):
        ShowBase.__init__(self)
        self.cTrav = CollisionTraverser()
        self.cTrav.showCollisions(self.render)
        self.__collisionHandler.addInPattern('%fn-into-%in')
        self.__collisionHandler.addOutPattern('%fn-out-%in')
        self.__gameState = GameState(self)

    def loadModel(self, modelPath):
        return self.loader.loadModel(modelPath)

    def setModelTexture(self, model, modelTexturePath):
        texture = self.loader.loadTexture(modelTexturePath)
        model.setTexture(texture, 1)

    def getTime(self):
        return self.__clock.getDt()

    def setColliderHandler(self, collider):
        self.cTrav.addCollider(collider, self.__collisionHandler)

    def defineCollisionEventHandling(self, fromCNode, intoCNode, collisionHandling):
        eventText = fromCNode + '-into-' + intoCNode
        self.accept(eventText, collisionHandling)

app = ArkanoidGame()
app.run()