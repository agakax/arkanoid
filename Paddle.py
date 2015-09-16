__author__ = 'Kamil'

from panda3d.core import LPoint3f, LVector3f
from pandac.PandaModules import KeyboardButton
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionNode
from math import sqrt

class Paddle(object):
    __gameEngine = None
    __position = LPoint3f(45, 5, 4)
    __scale = LPoint3f(1, 1, 1)
    __velocity = LVector3f(25.0, 0, 0)
    __reflectionVector = LVector3f(0, 0, 0)
    __reflectionDirection = LVector3f(0, 0, 0)
    __collider = None

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
        self.__collider = self.__paddle.attachNewNode(CollisionNode('paddleCNode'))
        minimum, maximum = self.__paddle.getTightBounds()
        sizes = (maximum - minimum)/2
        sizes = LPoint3f(sizes.getX()/self.__scale.getX(), sizes.getY()/self.__scale.getY(), sizes.getZ()/self.__scale.getZ())
        self.__collider.node().addSolid(CollisionSphere(0, 0, 0, max(sizes)))
        self.__gameEngine.setColliderHandler(self.__collider)
        self.__gameEngine.defineCollisionEventHandling('paddleCNode', 'boardWallsCNode', self.collideEvent)

    def collideEvent(self, entry):
        normal = entry.getContactNormal(entry.getIntoNodePath())
        self.__reflectionDirection = normal
        self.__reflectionVector = LVector3f(normal.getX()*self.__velocity.getX(), normal.getY()*self.__velocity.getY(), normal.getZ()*self.__velocity.getZ())
        self.__reflectionVector *= .05
        #self.__velocity = LPoint3f(self.__velocity.getX() * -1.0, self.__velocity.getY(), self.__velocity.getZ())

    def draw(self):
        paddleRoot = self.__gameEngine.render.attachNewNode('paddleRoot')
        self.__paddle.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        is_down = self.__gameEngine.mouseWatcherNode.is_button_down
        moveVector = LPoint3f(0, 0, 0)
        if self.reflectionVectorLength() > 0.1:
            moveVector = LVector3f(self.__reflectionDirection.getX()*self.__velocity.getX(), self.__reflectionDirection.getY()*self.__velocity.getY(), self.__reflectionDirection.getZ()*self.__velocity.getZ())
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
        self.__paddle.stash()
        self.__collider.removeNode()