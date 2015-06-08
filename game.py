__author__ = 'Kamila'
#from panda3d.core import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")


from direct.showbase.ShowBase import ShowBase


class ArkanoidGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()
        self.camera.setHpr(0, -45, 0)
        self.camera.setPos(25, -45, 70)
        # Load the environment model.
        self.environ = self.loader.loadModel("models/board")

        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(10, 10, 10)
        self.environ.setPos(0, 0, 0)
        boardTexture = self.loader.loadTexture('textures/limba.jpg')
        self.environ.setTexture(boardTexture, 1)
        # Load and transform the ball
        ballRoot = self.render.attachNewNode("ballRoot")
        ball = self.loader.loadModel("models/ball_v1")
        ball.setPos(25, 15, 4)
        ball.setScale(0.7, 0.7, 0.7)
        ballTexture = self.loader.loadTexture('textures/iron05.jpg')
        ball.setTexture(ballTexture, 1)
        ball.reparentTo(ballRoot)

app = ArkanoidGame()
app.run()