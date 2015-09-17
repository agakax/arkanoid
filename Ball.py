__author__ = 'Kamil'

from panda3d.core import LPoint3f
from pandac.PandaModules import CollisionNode, CollisionSphere

class Ball(object):
    __gameEngine = None
    __ball = None
    __position = LPoint3f(35, 25, 4)
    __velocity = LPoint3f(-20, 16, 0)
    __scale = LPoint3f(1, 1, 1)
    __collider = None

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.loadModel()
        self.setModelTexture()
        self.setModelParemeters()
        self.createCollider()
        self.setColliderHandler()
        self.defineCollisionEventHandling()

    def loadModel(self):
        self.__ball = self.__gameEngine.loadModel('models/ball_v1')

    def setModelTexture(self):
        self.__gameEngine.setModelTexture(self.__ball, 'textures/iron05.jpg')

    def setModelParemeters(self):
        self.__ball.setPos(self.__position)
        self.__ball.setScale(self.__scale)

    def createCollider(self):
        self.__collider = self.__ball.attachNewNode(CollisionNode('ballCNode'))
        radius = self.getBallRadius()
        self.__collider.node().addSolid(CollisionSphere(0, 0, 0, radius))

    def getBallRadius(self):
        minimum, maximum = self.__ball.getTightBounds()
        radius = (maximum - minimum)/2
        return max(radius.getX(), radius.getY(), radius.getZ())

    def setColliderHandler(self):
        self.__gameEngine.setColliderHandler(self.__collider)

    def defineCollisionEventHandling(self):
        self.__gameEngine.defineCollisionEventHandling('ballCNode', 'paddleCNode', self.collideEvent)
        self.__gameEngine.defineCollisionEventHandling('ballCNode', 'boardWallsCNode', self.collideEvent)

    def collideEvent(self, entry):
        normal = entry.getContactNormal(entry.getIntoNodePath())
        self.__velocity = self.getReflectionVector(normal)

    def getReflectionVector(self, normal):
        dotProduct = self.computeDotProduct(normal)
        subtrahend = LPoint3f(2*dotProduct*normal.getX(), 2*dotProduct*normal.getY(), 2*dotProduct*normal.getZ())
        return self.__velocity - subtrahend

    def computeDotProduct(self, normal):
        return sum(n*v for n,v in zip(normal, self.__velocity))

    def draw(self):
        self.__ball.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        moveVector = self.__velocity*elapsedTime
        self.__position = self.__ball.getPos() + moveVector
        self.__ball.setPos(self.__position)

    def destroy(self):
        self.__ball.stash()
        self.__collider.removeNode()
