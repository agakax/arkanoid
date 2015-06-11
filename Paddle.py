__author__ = 'Kamil'

from direct.showbase.DirectObject import DirectObject
from panda3d.core import Point3
from pandac.PandaModules import KeyboardButton

class Paddle(DirectObject):

    __position = Point3(25, 5, 4)
    __elapsedTime = 0.0
    __velocity = 8.0
    def __init__(self, parent):
        self.__parent = parent

        self.__paddleRoot = self.__parent.render.attachNewNode("paddleRoot")
        self.__paddle = self.__parent.loader.loadModel("models/ball_v1")

        self.__paddleTexture = self.__parent.loader.loadTexture("textures/iron05.jpg")
        self.__paddle.setTexture(self.__paddleTexture, 1)

    def draw(self):
        self.__paddle.reparentTo(self.__paddleRoot)

        self.__paddle.setScale(5, 0.7, 0.7)
        self.__paddle.setPos(self.__position)

    def update(self, elapsedTime):
        self.__elapsedTime = elapsedTime
        left_button = KeyboardButton.left()
        right_button = KeyboardButton.right()
        is_down = self.__parent.mouseWatcherNode.is_button_down
        if is_down(left_button):
            self.moveLeft()
        if is_down(right_button):
            self.moveRight()

    def moveLeft(self):
        self.__paddle.setPos(self.__paddle.getPos() + Point3(-self.__elapsedTime * self.__velocity, 0, 0))

    def moveRight(self):
        self.__paddle.setPos(self.__paddle.getPos() + Point3(self.__elapsedTime * self.__velocity, 0, 0))