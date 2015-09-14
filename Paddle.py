__author__ = 'Kamil'

from panda3d.core import LPoint3f
from pandac.PandaModules import KeyboardButton
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionNode

class Paddle(object):
    __gameEngine = None
    __position = LPoint3f(45, 5, 4)
    __scale = LPoint3f(5, 0.7, 0.7)
    __velocity = LPoint3f(8.0, 0, 0)
    __collider = None

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self.loadModel()
        self.setModelTexture()
        self.setModelParameters()
        self.createCollider()

        # Just to show collision sphere
        self.__collider.show()

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
        self.__collider.node().addSolid(CollisionSphere(0, 0, 0, 1))

    def draw(self):
        paddleRoot = self.__gameEngine.render.attachNewNode("paddleRoot")
        self.__paddle.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        is_down = self.__gameEngine.mouseWatcherNode.is_button_down
        moveVector = LPoint3f(0, 0, 0)
        if is_down(KeyboardButton.left()):
            moveVector = -self.__velocity*elapsedTime
        elif is_down(KeyboardButton.right()):
            moveVector = self.__velocity*elapsedTime
        self.__position += moveVector
        self.__paddle.setPos(self.__position)

    def destroy(self):
        self.__paddle.destroy()