__author__ = 'Kamila'
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import LVector3f
from panda3d.core import TransparencyAttrib

class ParallaxBackground(object):
    __gameEngine = None
    __base = None
    __gui = None
    background = None
    background1 = None
    background2 = None
    backgroundPos = LVector3f(0.0,0.0,0.0)
    background1Pos = LVector3f(0.0,0.0,0.0)
    background2Pos = LVector3f(0.0,0.0,0.0)


    speed1 = LVector3f(0.01,0.0,0.0)
    speed2 = LVector3f(0.02, 0.0, 0.0)
    speed3 = LVector3f(0.04, 0.0, 0.0)

    def __init__(self, gameEngine, base):
        self.__base = base
        self.__gameEngine = gameEngine
        self.loadBackground("textures/back.jpg", "textures/back1.png", "textures/back2.png")

    def loadBackground(self, imagepath, imagepath1, imagepath2):
        self.background = OnscreenImage(parent=self.__base.render2dp, image=imagepath, pos=self.backgroundPos)
        self.preserveImageAspect(self.background)
        self.background1 = OnscreenImage(parent=self.__base.render2dp, image=imagepath1, pos=self.backgroundPos)
        self.background1.setTransparency(TransparencyAttrib.MAlpha)
        self.preserveImageAspect(self.background1)
        self.background2 = OnscreenImage(parent=self.__base.render2dp, image=imagepath2, pos=self.backgroundPos)
        self.background2.setTransparency(TransparencyAttrib.MAlpha)
        self.preserveImageAspect(self.background2)
        self.__base.cam2dp.node().getDisplayRegion(0).setSort(-20) # Force the rendering to render the background image first (so that it will be put to the bottom of the scene since other models will be necessarily drawn on top)


    def preserveImageAspect(self, image):
        image.setScale(float(image.getTexture().getXSize())/self.__base.win.getXSize(), 1, float(image.getTexture().getYSize())/self.__base.win.getYSize())

    def updateBackground(self, movementX, elTime):
        if (movementX > 0):
            self.moveLeft(elTime)
        elif (movementX<0):
            self.moveRight(elTime)

    def moveLeft(self, deltaTime):
        newPosX = self.backgroundPos.x + (self.speed1.x) * deltaTime
        self.backgroundPos = LVector3f(newPosX, self.backgroundPos.y, self.backgroundPos.z)
        self.background.setPos(self.backgroundPos)
        newPos1X = self.background1Pos.x + (self.speed2.x) * deltaTime
        self.background1Pos = LVector3f(newPos1X, self.background1Pos.y, self.background1Pos.z)
        self.background1.setPos(self.background1Pos)
        newPos2X = self.background2Pos.x + (self.speed3.x) * deltaTime
        self.background2Pos = LVector3f(newPos2X, self.background2Pos.y, self.background2Pos.z)
        self.background2.setPos(self.background2Pos)

    def moveRight(self, deltaTime):
        newPosX = self.backgroundPos.x + -(self.speed1.x) * deltaTime
        self.backgroundPos = LVector3f(newPosX, self.backgroundPos.y, self.backgroundPos.z)
        self.background.setPos(self.backgroundPos)
        newPos1X = self.background1Pos.x + -(self.speed2.x) * deltaTime
        self.background1Pos = LVector3f(newPos1X, self.background1Pos.y, self.background1Pos.z)
        self.background1.setPos(self.background1Pos)
        newPos2X = self.background2Pos.x + -(self.speed3.x) * deltaTime
        self.background2Pos = LVector3f(newPos2X, self.background2Pos.y, self.background2Pos.z)
        self.background2.setPos(self.background2Pos)
