__author__ = 'Kamil'

class Board(object):
    def __init__(self, parent):

        self.__parent = parent
        # Disable the camera trackball controls.
        #self.disableMouse()
        self.__parent.camera.setHpr(0, -45, 0)
        self.__parent.camera.setPos(25, -45, 40)
        # Load the environment model.
        self.__environ = self.__parent.loader.loadModel("models/board")
        self.__boardTexture = self.__parent.loader.loadTexture('textures/limba.jpg')
        self.__environ.setTexture(self.__boardTexture, 1)

    def draw(self):
        # Reparent the model to render.
        self.__environ.reparentTo(self.__parent.render)
        # Apply scale and position transforms on the model.
        self.__environ.setScale(10, 10, 10)
        self.__environ.setPos(0, 0, 0)
