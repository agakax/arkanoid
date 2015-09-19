__author__ = 'Kamil'

from panda3d.core import LPoint3f, LVector3f, BitMask32
from pandac.PandaModules import CollisionNode, CollisionBox, CollisionRay, ActorNode, CollisionSphere, CollisionPlane, Plane
from Board import Board
from MathFunctions import *


class Block(object):
    BLOCK_MASK = BitMask32.bit(3)
    SCALE = 3
    _gameEngine = None
    _block = None
    _position = LPoint3f(0, 0, 0)
    _points = 0
    _durability = 0
    _hitCollider = None
    _rayCollider = None
    _ceilCollider = None

    def __init__(self, gameEngine, blockId):
        self._gameEngine = gameEngine

    def loadModel(self, modelPath):
        self._block = self._gameEngine.loadModel(modelPath)

    def setModelTexture(self, texturePath):
        self._gameEngine.setModelTexture(self._block, texturePath)

    def setModelParameters(self, position):
        self._position = position
        self._block.setPos(self._position)
        self._block.setScale(self.SCALE)
        self._block.setCollideMask(BitMask32.allOff())

    def createHitCollider(self, blockId):
        self._hitCollider = self._block.attachNewNode(CollisionNode('blockCNode' + str(blockId)))
        minPos, maxPos = self._block.getTightBounds()
        sizes = (maxPos - minPos)/(2*self.SCALE)
        self._hitCollider.node().addSolid(CollisionBox(LPoint3f(0, 0, 0), sizes.getX(), sizes.getY(), sizes.getZ()))
        self._hitCollider.node().setIntoCollideMask(self.BLOCK_MASK)
        self._hitCollider.node().setFromCollideMask(BitMask32.allOff())

    def createCeilCollider(self, blockId):
        self._ceilCollider = self._block.find("**/ceil_collider")
        self._ceilCollider.node().setFromCollideMask(BitMask32.allOff())
        self._ceilCollider.node().setIntoCollideMask(Board.FLOOR_MASK)

    def createRay(self, blockId):
        ray = CollisionRay(0, 0, 0, 0, 0, -1)
        self._rayCollider = self._block.attachNewNode(CollisionNode('rayCollider'))
        self._rayCollider.node().addSolid(ray)
        self._rayCollider.node().setFromCollideMask(Board.FLOOR_MASK)
        self._rayCollider.node().setIntoCollideMask(BitMask32.allOff())

    def setFallCollideHandling(self):
        self._gameEngine.addFloorColliders(self._rayCollider, self._block)
        self._gameEngine.setFloorColliderHandler(self._rayCollider)

    def draw(self):
        self._block.reparentTo(self._gameEngine.render)

    def update(self, elapsedTime):
        pass

    def destroy(self):
        self._block.removeNode()
        #self._hitCollider.removeNode()
        #if self._ceilCollider != None:
        #    self._ceilCollider.removeNode()
        #self._rayCollider.removeNode()