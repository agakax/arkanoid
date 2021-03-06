__author__ = 'Kamil'
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from EnumGameStates import EnumGameStates
from pandac.PandaModules import KeyboardButton
class Enum(tuple): __getattr__ = tuple.index

class EnumMenuOptions(Enum):
    NEW_GAME = 0
    QUIT = 1

class GUI(object):
    __selected = None
    __gameEngine = None
    __gameState = None
    __base = None
    __screenImage = None
    __titleImage = None
    __newGameImage = None
    __selectedImage = None
    __quitImage = None
    __screenImagePath = "textures/back.jpg"
    __titleImagePath = "textures/title.png"
    __newGameImagePath = "textures/newgame.png"
    __quitImagePath = "textures/quit.png"
    __selectedImagePath = "textures/selected.png"
    __gameOverText = None
    __backToMenuText = None
    __tryAgainText = None

    def __init__(self, gameEngine, base, gameState):
        self.__gameEngine = gameEngine
        self.__base = base
        self.__gameState = gameState
        self.__selected = EnumMenuOptions.NEW_GAME

    def showMenu(self):
        self.__screenImage = OnscreenImage(parent=self.__base.render2d, image=self.__screenImagePath, pos=(0,0,0))
        self.preserveImageAspect(self.__screenImage)

        self.__selectedImage = OnscreenImage(parent=self.__base.render2d, image=self.__selectedImagePath)
        self.__selectedImage.setTransparency(TransparencyAttrib.MAlpha)
        self.preserveImageAspect(self.__selectedImage)

        self.__titleImage = OnscreenImage(parent=self.__base.render2d, image=self.__titleImagePath)
        self.__titleImage.setTransparency(TransparencyAttrib.MAlpha)
        self.__titleImage.setPos(0,0,0.5)
        self.preserveImageAspect(self.__titleImage)

        self.__newGameImage = OnscreenImage(parent=self.__base.render2d, image=self.__newGameImagePath)
        self.__newGameImage.setTransparency(TransparencyAttrib.MAlpha)
        self.__newGameImage.setPos(0,0,0.0)
        self.preserveImageAspect(self.__newGameImage)

        self.__quitImage = OnscreenImage(parent=self.__base.render2d, image=self.__quitImagePath)
        self.__quitImage.setTransparency(TransparencyAttrib.MAlpha)
        self.__quitImage.setPos(0,0,-0.2)
        self.preserveImageAspect(self.__quitImage)

        self.changeSelected(EnumMenuOptions.NEW_GAME)

    def hideMenu(self):
        self.__screenImage.removeNode()
        self.__titleImage.removeNode()
        self.__newGameImage.removeNode()
        self.__quitImage.removeNode()
        self.__selectedImage.removeNode()

    def hideGameOver(self):
        if self.__gameOverText != None:
            self.__gameOverText.removeNode()
        if self.__tryAgainText != None:
            self.__tryAgainText.removeNode()
        if self.__backToMenuText != None:
            self.__backToMenuText.removeNode()

    def update (self, elapsedTime):
        is_down = self.__base.mouseWatcherNode.is_button_down
        if  (is_down(KeyboardButton.up()) and (self.__selected > 0)):
            self.changeSelected(self.__selected - 1)
        elif (is_down(KeyboardButton.down()) and (self.__selected < 1)):
            self.changeSelected(self.__selected + 1)
        elif is_down(KeyboardButton.enter()):
            self.runSelectedOption()
        pass

    def runSelectedOption(self):
        if self.__selected == EnumMenuOptions.NEW_GAME:
            self.hideMenu()
            self.__gameState.setGameState(EnumGameStates.PLAY)
        elif self.__selected == EnumMenuOptions.QUIT:
            self.__gameState.setGameState(EnumGameStates.EXITING)

    def backToMenu(self):
        self.hideGameOver()
        self.__gameState.setGameState(EnumGameStates.MENU)

    def preserveImageAspect(self, image):
        image.setScale(float(image.getTexture().getXSize())/self.__base.win.getXSize(), 1, float(image.getTexture().getYSize())/self.__base.win.getYSize())

    def changeSelected(self, menuOption):
        if self.__gameState.getGameState() == EnumGameStates.MENU:
            if menuOption == EnumMenuOptions.NEW_GAME:
                self.__selectedImage.setPos(self.__newGameImage.getPos())
            elif menuOption == EnumMenuOptions.QUIT:
                self.__selectedImage.setPos(self.__quitImage.getPos())
            self.__selected = menuOption
        else:
            pass

    def showGameOver(self):
        self.__gameOverText =  OnscreenText(text = 'GAME OVER',
                                            pos = (0.0, 0.4),
                                            scale = 0.1,
                                            parent = self.__base.render2d,
                                            fg = (1,0,0,1),
                                            shadow = (0,0,0,1))
        self.__tryAgainText =  OnscreenText(text = '"R" - try this level again',
                                            pos = (0.0, 0.2),
                                            scale = 0.07,
                                            parent = self.__base.render2d,
                                            fg = (1,0,0,1),
                                            shadow = (0,0,0,1))
        self.__backToMenuText =  OnscreenText(text = '"Esc" - back to menu',
                                            pos = (0.0, 0.0),
                                            scale = 0.07,
                                            parent = self.__base.render2d,
                                            fg = (1,0,0,1),
                                            shadow = (0,0,0,1))



