__author__ = 'Kamil'

from panda3d.core import LPoint3f
from pandac.PandaModules import CollisionNode, CollisionBox
from pandac.PandaModules import ModelNode

class Block(object):
    _gameEngine = None
    _block = None
    _position = LPoint3f(0, 0, 0)
    _scale = LPoint3f(1, 1, 1)
    _points = 0
    _durability = 0
    _hitCollider = None
    _floorCollider = None

    def __init__(self, gameEngine):
        self._gameEngine = gameEngine

    def loadModel(self, modelPath):
        self._block = self._gameEngine.loadModel(modelPath)

    def setModelTexture(self, texturePath):
        self._gameEngine.setModelTexture(self._block, texturePath)

    def setModelParameters(self, position):
        self._position = position
        self._block.setPos(self._position)
        self._block.setScale(self._scale)

    def createCollider(self, colliderNodeName):
        self._hitCollider = self._block.attachNewNode(CollisionNode(colliderNodeName))
        self._block.setPos(LPoint3f(0, 0, 0))
        minPos, maxPos = self._block.getTightBounds()
        self._block.setPos(self._position)
        self._hitCollider.node().addSolid(CollisionBox(minPos, maxPos))

    def draw(self):
        self._block.reparentTo(self._gameEngine.render)

    def update(self, elapsedTime):
        pass

    def destroy(self):
        self._block.stash()
        self._hitCollider.removeNode()


