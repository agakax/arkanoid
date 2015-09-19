__author__ = 'Kamila'
#from panda3d.core import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject, CollisionHandlerEvent, CollisionTraverser, CollisionHandlerFloor, CollisionHandlerPusher
from pandac.PandaModules import PointLight
from GameState import GameState

class ArkanoidGame(ShowBase):
    __clock = ClockObject.getGlobalClock()
    __collisionHandler = CollisionHandlerEvent()
    __collisionFloorHandler = CollisionHandlerFloor()
    __collisionWallHandlerPusher = CollisionHandlerPusher()
    __gameState = None
    def __init__(self):
        ShowBase.__init__(self)
        self.cTrav = CollisionTraverser()
        self.setGravity()
        self.setLight()
        self.__collisionHandler.addInPattern('%fn-into-%in')
        self.__collisionHandler.addInPattern('%fn-into')
        self.__gameState = GameState(self)

    def setGravity(self):
        self.__collisionFloorHandler.setMaxVelocity(15)
        self.__collisionFloorHandler.setOffset(1.0)

    def setLight(self):
        pLight = PointLight('pLight')
        plnp = self.render.attachNewNode(pLight)
        plnp.setPos(37, 10, 15)
        self.render.setLight(plnp)

    def loadModel(self, modelPath):
        return self.loader.loadModel(modelPath)

    def setModelTexture(self, model, modelTexturePath):
        texture = self.loader.loadTexture(modelTexturePath)
        model.setTexture(texture, 1)

    def setColliderHandler(self, collider):
        self.cTrav.addCollider(collider, self.__collisionHandler)

    def addFloorColliders(self, ray, node):
        self.__collisionFloorHandler.addCollider(ray, node)

    def setFloorColliderHandler(self, collider):
        self.cTrav.addCollider(collider, self.__collisionFloorHandler)

    def addWallColliders(self, collider, node):
        self.__collisionWallHandlerPusher.addCollider(collider, node)

    def setWallColliderHandler(self, collider):
        self.cTrav.addCollider(collider, self.__collisionWallHandlerPusher)

    def defineCollisionEventHandling(self, fromCNode, intoCNode, collisionHandling):
        eventText = fromCNode + '-into-' + intoCNode
        self.accept(eventText, collisionHandling)

    def defineCollisionEventHandlingFrom(self, fromCNode, collisionHandling):
        eventText = fromCNode + '-into'
        self.accept(eventText, collisionHandling)

    def generateEvent(self, event, args):
        self.messenger.send(event, args)

    def getTime(self):
        return self.__clock.getDt()

app = ArkanoidGame()
app.run()