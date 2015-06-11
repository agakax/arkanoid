__author__ = 'Kamil'

class Ball(object):
    def __init__(self, parent):
        self.__parent = parent
        # Load and transform the __ball
        self.__ballRoot = self.__parent.render.attachNewNode("ballRoot")
        self.__ball = self.__parent.loader.loadModel("models/ball_v1")

        self.__ballTexture = self.__parent.loader.loadTexture('textures/iron05.jpg')
        self.__ball.setTexture(self.__ballTexture, 1)


    def draw(self):
        self.__ball.reparentTo(self.__ballRoot)
        self.__ball.setPos(25, 15, 4)
        self.__ball.setScale(0.7, 0.7, 0.7)