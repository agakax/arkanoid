__author__ = 'Kamila'
#from panda3d.core import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject, CollisionHandlerEvent, CollisionTraverser, CollisionHandlerGravity
from pandac.PandaModules import PointLight
from GameState import GameState

class ArkanoidGame(ShowBase):
    __clock = ClockObject.getGlobalClock()
    __collisionHandler = CollisionHandlerEvent()
    __collisionFloorHandler = CollisionHandlerGravity()
    __gameState = None
    def __init__(self):
        ShowBase.__init__(self)
        self.cTrav = CollisionTraverser()
        self.setGravity()
        self.setLight()
        self.__collisionHandler.addInPattern('%fn-into-%in')
        self.__gameState = GameState(self)

    def setGravity(self):
        self.__collisionFloorHandler.setGravity(9.81+15)
        self.__collisionFloorHandler.setMaxVelocity(100)

    def setLight(self):
        pLight = PointLight('pLight')
        plnp = self.render.attachNewNode(pLight)
        plnp.setPos(37, 10, 15)
        self.render.setLight(plnp)

    def attachNewNode(self, node):
        return self.render.attachNewNode(node)

    def loadModel(self, modelPath):
        return self.loader.loadModel(modelPath)

    def setModelTexture(self, model, modelTexturePath):
        texture = self.loader.loadTexture(modelTexturePath)
        model.setTexture(texture, 1)

    def setColliderHandler(self, collider):
        self.cTrav.addCollider(collider, self.__collisionHandler)

    def setFloorColliderHandler(self, collider):
        self.cTrav.addCollider(collider, self.__collisionFloorHandler)

    def defineCollisionEventHandling(self, fromCNode, intoCNode, collisionHandling):
        eventText = fromCNode + '-into-' + intoCNode
        self.accept(eventText, collisionHandling)

    def getTime(self):
        return self.__clock.getDt()

app = ArkanoidGame()
app.run()