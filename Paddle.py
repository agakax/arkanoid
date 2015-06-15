__author__ = 'Kamil'

from panda3d.core import LPoint3f
from pandac.PandaModules import KeyboardButton
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionNode

class Paddle(object):

    __gameEngine = None
    __position = None
    __scale = None
    __elapsedTime = None
    __velocity = None
    __leftButton = None
    __rightButton = None
    __collisionNodePath = None

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.loadModel()
        self.initValues()
        self.setModelTexture()
        self.setModelParameters()
        collisionSphere = self.createCollisionSphere()
        self.addCollisionSolidToNode(collisionSphere)

        # Just to show collision sphere
        self.__collisionNodePath.show()

    def initValues(self):
        self.__position = LPoint3f(25, 5, 4)
        self.__scale = LPoint3f(5, 0.7, 0.7)
        self.__velocity = LPoint3f(8.0, 0, 0)
        self.__rightButton = KeyboardButton.right()
        self.__leftButton = KeyboardButton.left()
        self.__collisionNodePath = self.__paddle.attachNewNode(CollisionNode('solids'))

    def loadModel(self):
        self.__paddle = self.__gameEngine.loader.loadModel("models/ball_v1")

    def setModelTexture(self):
        paddleTexture = self.__gameEngine.loader.loadTexture("textures/iron05.jpg")
        self.__paddle.setTexture(paddleTexture, 1)

    def setModelParameters(self):
        self.__paddle.setScale(self.__scale)
        self.__paddle.setPos(self.__position)

    def createCollisionSphere(self):
        min, max = self.__paddle.getTightBounds()
        length = (max - min)/2
        return CollisionSphere(0, 0, 0, length.getY() + 1)

    def addCollisionSolidToNode(self, collisionSolid):
        self.__collisionNodePath.node().addSolid(collisionSolid)

    def draw(self):
        paddleRoot = self.__gameEngine.render.attachNewNode("paddleRoot")
        self.__paddle.reparentTo(paddleRoot)

    def update(self, elapsedTime):
        self.__elapsedTime = elapsedTime
        self.__position = self.__paddle.getPos()
        is_down = self.__gameEngine.mouseWatcherNode.is_button_down
        if is_down(self.__leftButton):
            self.moveLeft()
        if is_down(self.__rightButton):
            self.moveRight()

    def moveLeft(self):
        moveVector = -self.__velocity*self.__elapsedTime
        self.__paddle.setPos(self.__position + moveVector)

    def moveRight(self):
        moveVector = self.__velocity*self.__elapsedTime
        self.__paddle.setPos(self.__position + moveVector)