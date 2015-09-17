__author__ = 'Kamil'

from panda3d.core import LPoint3f, LVector3f, BitMask32
from pandac.PandaModules import CollisionNode, CollisionBox, CollisionRay, ActorNode, CollisionSphere, CollisionPolygon
from Board import Board
from MathFunctions import *


class Block(object):
    _gameEngine = None
    _blockNP = None
    _block = None
    _position = LPoint3f(0, 0, 0)
    _scale = LPoint3f(1, 1, 1)
    _points = 0
    _durability = 0
    _hitCollider = None
    _floorCollider = None
    _rayCollider = None
    _ceilCollider = None

    def __init__(self, gameEngine, blockId):
        self._gameEngine = gameEngine
        self._blockNP = self._gameEngine.attachNewNode(ActorNode('blockNP' + str(blockId)))

    def loadModel(self, modelPath):
        self._block = self._gameEngine.loadModel(modelPath)
        self._block.reparentTo(self._blockNP)

    def setModelTexture(self, texturePath):
        self._gameEngine.setModelTexture(self._block, texturePath)

    def setModelParameters(self, position):
        self._position = position
        self._block.setPos(0, 0, 1)
        self._block.setCollideMask(BitMask32.allOff())
        self._blockNP.setPos(self._position)
        self._blockNP.setScale(self._scale)

    def createHitCollider(self, blockId):
        self._hitCollider = self._block.attachNewNode(CollisionNode('blockCNode' + str(blockId)))
        minPos, maxPos = self._block.getTightBounds()
        sizes = (maxPos - minPos)/2
        self._hitCollider.node().addSolid(CollisionBox(LPoint3f(0, 0, 0), sizes.getX(), sizes.getY(), sizes.getZ()))
        self._hitCollider.node().setCollideMask(BitMask32.allOff())

    def createCeilCollider(self, blockId):
        self._ceilCollider = self._blockNP.attachNewNode(CollisionNode('blockCeil' + str(blockId)))
        minPos, maxPos = self._blockNP.getTightBounds()
        sizes = LPoint3f(maxPos - minPos)/2
        point1 = LPoint3f(multiplyVectorsElements(sizes, LPoint3f(-1, -1, 2)))
        point2 = LPoint3f(multiplyVectorsElements(sizes, LPoint3f(1, -1, 2)))
        point3 = LPoint3f(multiplyVectorsElements(sizes, LPoint3f(1, 1, 2)))
        point4 = LPoint3f(multiplyVectorsElements(sizes, LPoint3f(-1, 1, 2)))
        polygon = CollisionPolygon(point1, point2, point3, point4)
        self._ceilCollider.node().addSolid(polygon)
        self._ceilCollider.node().setFromCollideMask(BitMask32.allOff())
        self._ceilCollider.node().setIntoCollideMask(Board.FLOOR_MASK)
        polygon.setTangible(0)

    def createFloorCollider(self, blockId):
        self._floorCollider = self._blockNP.attachNewNode(CollisionNode('blockSensor' + str(blockId)))
        sensor = CollisionSphere(0, 0, 0, .5)
        self._floorCollider.node().addSolid(sensor)
        self._floorCollider.node().setFromCollideMask(Board.FLOOR_MASK)
        self._floorCollider.node().setIntoCollideMask(BitMask32.allOff())
        sensor.setTangible(0)

    def createRay(self, blockId):
        ray = CollisionRay(0, 0, 1, 0, 0, -1)
        self._rayCollider = self._blockNP.attachNewNode(CollisionNode('rayCollider' + str(blockId)))
        self._rayCollider.node().addSolid(ray)
        self._rayCollider.node().setFromCollideMask(Board.FLOOR_MASK)
        self._rayCollider.node().setIntoCollideMask(BitMask32.allOff())

    def setFallCollideHandling(self):
        self._gameEngine.addFloorColliders(self._rayCollider, self._blockNP)
        self._gameEngine.setFloorColliderHandler(self._rayCollider)
        self._gameEngine.setColliderHandler(self._floorCollider)

    def draw(self):
        self._blockNP.reparentTo(self._gameEngine.render)

    def update(self, elapsedTime):
        pass

    def destroy(self):
        self._blockNP.stash()
        self._hitCollider.removeNode()
        self._ceilCollider.removeNode()
        self._floorCollider.removeNode()
        self._rayCollider.removeNode()


