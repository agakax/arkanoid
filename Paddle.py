__author__ = 'Kamil'

from panda3d.core import LPoint3f, LVector3f, BitMask32
from pandac.PandaModules import KeyboardButton
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionNode
from MathFunctions import *
from math import sqrt
from Board import Board

class Paddle(object):
    PADDLE_MASK = BitMask32.bit(4)
    __gameEngine = None
    __position = LPoint3f(45, 5, 4)
    __scale = LPoint3f(1, 1, 1)
    __velocity = LVector3f(25.0, 0, 0)
    __reflectionVector = LVector3f(0, 0, 0)
    __reflectionDirection = LVector3f(0, 0, 0)
    __ballCollider = None
    __wallCollider = None

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.loadModel()
        self.setModelTexture()
        self.setModelParameters()
        self.createCollider()

    def loadModel(self):
        self.__paddle = self.__gameEngine.loadModel('models/ball_v1')

    def setModelTexture(self):
        self.__gameEngine.setModelTexture(self.__paddle, 'textures/iron05.jpg')

    def setModelParameters(self):
        self.__paddle.setScale(self.__scale)
        self.__paddle.setPos(self.__position)

    def createCollider(self):
        self.__ballCollider = self.__paddle.attachNewNode(CollisionNode('paddleBallCNode'))
        minimum, maximum = self.__paddle.getTightBounds()
        sizes = (maximum - minimum)/2
        sizes = LPoint3f(divideVectorsElements(sizes, self.__scale))
        self.__ballCollider.node().addSolid(CollisionSphere(0, 0, 0, max(sizes)))
        self.__ballCollider.node().setIntoCollideMask(self.PADDLE_MASK)
        self.__ballCollider.node().setFromCollideMask(BitMask32.allOff())

        self.__wallCollider = self.__paddle.attachNewNode(CollisionNode('paddleWallCNode'))
        self.__wallCollider.node().addSolid(CollisionSphere(0, 0, 0, max(sizes)))
        self.__wallCollider.node().setIntoCollideMask(BitMask32.allOff())
        self.__wallCollider.node().setFromCollideMask(Board.WALL_MASK)

        self.__gameEngine.setColliderHandler(self.__ballCollider)
        self.__gameEngine.setColliderHandler(self.__wallCollider)
        self.__gameEngine.defineCollisionEventHandling('paddleWallCNode', 'boardWallsCNode', self.collideEvent)

    def collideEvent(self, entry):
        normal = entry.getContactNormal(entry.getIntoNodePath())
        self.__reflectionDirection = normal
        self.__reflectionVector = LVector3f(normal.getX()*self.__velocity.getX(), normal.getY()*self.__velocity.getY(), normal.getZ()*self.__velocity.getZ())
        self.__reflectionVector *= .05

    def draw(self):
        self.__paddle.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        is_down = self.__gameEngine.mouseWatcherNode.is_button_down
        moveVector = LPoint3f(0, 0, 0)
        if self.reflectionVectorLength() > 0.5:
            moveVector = LVector3f(multiplyVectorsElements(self.__reflectionDirection, self.__velocity))
            moveVector *= elapsedTime
            self.__reflectionVector -= moveVector
        elif is_down(KeyboardButton.left()):
            moveVector = -self.__velocity*elapsedTime
        elif is_down(KeyboardButton.right()):
            moveVector = self.__velocity*elapsedTime
        self.__position += moveVector
        self.__paddle.setPos(self.__position)

    def reflectionVectorLength(self):
        return sqrt(sum(i*i for i in self.__reflectionVector))

    def destroy(self):
        self.__paddle.removeNode()
        #self.__ballCollider.removeNode()