__author__ = 'Kamil'

from panda3d.core import LPoint3f
from pandac.PandaModules import CollisionNode, CollisionBox, CollisionRay, ActorNode, CollisionSphere

class Block(object):
    _gameEngine = None
    _blockNP = None
    _block = None
    _position = LPoint3f(0, 0, 0)
    _scale = LPoint3f(1, 1, 1)
    _points = 0
    _durability = 0
    _hitCollider = None
    _floorSensor = None
    _rayCollider = None

    def __init__(self, gameEngine, blockId):
        self._gameEngine = gameEngine
        self._blockNP = self._gameEngine.attachNewNode(ActorNode('block' + blockId + 'NP'))

    def loadModel(self, modelPath):
        self._block = self._gameEngine.loadModel(modelPath)
        self._block.reparentTo(self._blockNP)

    def setModelTexture(self, texturePath):
        self._gameEngine.setModelTexture(self._block, texturePath)

    def setModelParameters(self, position):
        self._position = position
        self._blockNP.setPos(self._position)
        #self._blockNP.setScale(self._scale)
        self._block.setPos(0, 0, 1)
        #self._block.setScale(1, 1, 1)

    def createHitCollider(self, colliderNodeName):
        self._hitCollider = self._block.attachNewNode(CollisionNode(colliderNodeName + 'CNode'))
        minPos, maxPos = self._block.getTightBounds()
        sizes = (maxPos - minPos)/2
        self._hitCollider.node().addSolid(CollisionBox(LPoint3f(0, 0, 0), sizes.getX(), sizes.getY(), sizes.getZ()))

    def createFloorSensor(self, colliderNodeName):
        self._floorSensor = self._blockNP.attachNewNode(CollisionNode(colliderNodeName + 'Floor'))
        collisionBox = CollisionSphere(0, 0, 0, 1.2)
        self._floorSensor.node().addSolid(collisionBox)
        collisionBox.setTangible(0)

    def createRayCollider(self, colliderNodeName):
        ray = CollisionRay(0, 0, 1, 0, 0, -1)
        self._rayCollider = self._blockNP.attachNewNode(CollisionNode(colliderNodeName + 'Ray'))
        self._rayCollider.node().addSolid(ray)
        self._gameEngine.addFloorColliders(self._rayCollider, self._blockNP)

    def setCollidersHandlers(self):
        self._gameEngine.setFloorColliderHandler(self._rayCollider)
        #self._gameEngine.setColliderHandler(self._hitCollider)
        self._gameEngine.setColliderHandler(self._floorSensor)

    def draw(self):
        self._blockNP.reparentTo(self._gameEngine.render)

    def update(self, elapsedTime):
        pass

    def destroy(self):
        self._block.stash()
        self._hitCollider.removeNode()


