__author__ = 'Kamil'

from panda3d.core import LPoint3f
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionNode

class Ball(object):
    __gameEngine = None
    __position = None
    __velocity = None
    __elapsedTime = None
    __collisionNodePath = None

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.loadModel()
        self.initValues()
        self.setModelTexture()
        self.setModelParemeters()
        collisionSphere = self.createCollisionSphere()
        self.addCollisionSphereToNode(collisionSphere)

        # Just to show collision sphere
        self.__collisionNodePath.show()

    def initValues(self):
        self.__position = LPoint3f(25, 15, 4)
        self.__velocity = LPoint3f(1.0, 0.5, 0)
        self.__scale = LPoint3f(0.7, 0.7, 0.7)
        self.__collisionNodePath = self.__ball.attachNewNode(CollisionNode('solids'))

    def loadModel(self):
        self.__ball = self.__gameEngine.loader.loadModel("models/ball_v1")

    def setModelTexture(self):
        ballTexture = self.__gameEngine.loader.loadTexture('textures/iron05.jpg')
        self.__ball.setTexture(ballTexture, 1)

    def setModelParemeters(self):
        self.__ball.setPos(self.__position)
        self.__ball.setScale(self.__scale)

    def createCollisionSphere(self):
        min, max = self.__ball.getTightBounds()
        radius = (max - min)/2
        return CollisionSphere(0, 0, 0, radius.getX() + 1)

    def addCollisionSphereToNode(self, collisionSolid):
        self.__collisionNodePath.node().addSolid(collisionSolid)

    def draw(self):
        ballRoot = self.__gameEngine.render.attachNewNode("ballRoot")
        self.__ball.reparentTo(ballRoot)


    def update(self, elapsedTime):
        self.__elapsedTime = elapsedTime
        self.__position = self.__ball.getPos()
        self.moveBall()

    def moveBall(self):
        moveVector = self.__velocity*self.__elapsedTime
        self.__ball.setPos(self.__position + moveVector)

    def detectCollision(self, objects):
        pass