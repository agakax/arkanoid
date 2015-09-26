__author__ = 'Kamila'
#from panda3d.core import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import ClockObject, CollisionHandlerEvent, CollisionTraverser, CollisionHandlerFloor
from pandac.PandaModules import PointLight, AmbientLight
from panda3d.core import LPoint3f, VBase4

from GameState import GameState

class ArkanoidGame(DirectObject):
    __clock = ClockObject.getGlobalClock()
    __collisionHandler = CollisionHandlerEvent()
    __collisionFloorHandler = CollisionHandlerFloor()
    __gameState = None
    def __init__(self):
        #ShowBase.__init__(self)

        base.cTrav = CollisionTraverser()
        base.cTrav.setRespectPrevTransform(True)
        self.setGravity()
        self.setLight()
        self.__collisionHandler.addInPattern('%fn-into-%in')
        self.__collisionHandler.addInPattern('%fn-into')
        self.__gameState = GameState(self, base)

    def setGravity(self):
        self.__collisionFloorHandler.setMaxVelocity(15)
        self.__collisionFloorHandler.setOffset(1.0)

    def setLight(self):
        pLight = PointLight('pLight')
        plnp = base.render.attachNewNode(pLight)
        plnp.setPos(37, 10, 15)
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.25, 0.25, 1))
        alnp = base.render.attachNewNode(alight)
        base.render.setLight(plnp)
        base.render.setLight(alnp)

    def loadModel(self, modelPath):
        return base.loader.loadModel(modelPath)

    def setModelTexture(self, model, modelTexturePath):
        texture = base.loader.loadTexture(modelTexturePath)
        model.setTexture(texture, 1)

    def setColliderHandler(self, collider):
        base.cTrav.addCollider(collider, self.__collisionHandler)

    def addFloorColliders(self, ray, node):
        self.__collisionFloorHandler.addCollider(ray, node)

    def setFloorColliderHandler(self, collider):
        base.cTrav.addCollider(collider, self.__collisionFloorHandler)

    def defineIntoCollisionEventHandling(self, fromCNode, intoCNode, collisionHandling):
        eventText = fromCNode + '-into-' + intoCNode
        self.accept(eventText, collisionHandling)

    def defineIntoCollisionEventHandlingFrom(self, fromCNode, collisionHandling):
        eventText = fromCNode + '-into'
        base.accept(eventText, collisionHandling)

    def generateEvent(self, event, args):
        base.messenger.send(event, args)

    def getTime(self):
        return self.__clock.getDt()



app = ArkanoidGame()
base.run()