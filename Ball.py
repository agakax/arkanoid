__author__ = 'Kamil'

from panda3d.core import LPoint3f, BitMask32
from pandac.PandaModules import CollisionNode, CollisionSphere
from Board import Board
from Block import Block
from Paddle import Paddle

class Ball(object):
    SCALE = 1
    __gameEngine = None
    __ball = None
    __position = None
    __velocity = None
    __wallCollider = None
    __blockCollider = None
    __paddleCollider = None
    refl = False

    def __init__(self, gameEngine):
        self.__gameEngine = gameEngine
        self. __position = LPoint3f(35, 25, 4)
        self.__velocity = LPoint3f(-20, 0, 0)#LPoint3f(0, 0, 0) #
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
        self.__ball.setScale(self.SCALE)

    def createCollider(self):
        self.__wallCollider = self.__ball.attachNewNode(CollisionNode('ballWallCNode'))
        radius = self.getBallRadius()
        self.__wallCollider.node().addSolid(CollisionSphere(0, 0, 0, radius))
        self.__wallCollider.node().setFromCollideMask(Board.WALL_MASK)
        self.__wallCollider.node().setIntoCollideMask(BitMask32.allOff())
        self.__blockCollider = self.__ball.attachNewNode(CollisionNode('ballBlockCNode'))
        self.__blockCollider.node().addSolid(CollisionSphere(0, 0, 0, radius))
        self.__blockCollider.node().setFromCollideMask(Block.BLOCK_MASK)
        self.__blockCollider.node().setIntoCollideMask(BitMask32.allOff())
        self.__paddleCollider = self.__ball.attachNewNode(CollisionNode('ballPaddleCNode'))
        self.__paddleCollider.node().addSolid(CollisionSphere(0, 0, 0, radius))
        self.__paddleCollider.node().setFromCollideMask(Paddle.PADDLE_MASK)
        self.__paddleCollider.node().setIntoCollideMask(BitMask32.allOff())

    def getBallRadius(self):
        minimum, maximum = self.__ball.getTightBounds()
        radius = (maximum - minimum)/2
        return max(radius.getX(), radius.getY(), radius.getZ())

    def setColliderHandler(self):
        self.__gameEngine.setColliderHandler(self.__paddleCollider)
        self.__gameEngine.setColliderHandler(self.__wallCollider)
        self.__gameEngine.setColliderHandler(self.__blockCollider)

    def defineCollisionEventHandling(self):
        self.__gameEngine.defineIntoCollisionEventHandling('ballPaddleCNode', 'paddleBallCNode', self.collideEvent)
        self.__gameEngine.defineIntoCollisionEventHandling('ballWallCNode', 'boardWallsCNode', self.collideEvent)
        self.__gameEngine.defineIntoCollisionEventHandlingFrom('ballBlockCNode', self.hitBlock)
       # self.__gameEngine.defineAgainCollisionEventHangling('ballPaddleCNode', 'boardWallsCNode', self)

    def collideEvent(self, entry):
        normal = entry.getContactNormal(entry.getIntoNodePath())
        self.__velocity = self.getReflectionVector(normal)

    def hitBlock(self, entry):
        self.collideEvent(entry)
        self.__gameEngine.generateEvent('hitBlock', [entry])

    def getReflectionVector(self, normal):
        dotProduct = self.computeDotProduct(normal)
        subtrahend = LPoint3f(2*dotProduct*normal[0], 2*dotProduct*normal[1], 2*dotProduct*normal[2])
        return self.__velocity - subtrahend

    def computeDotProduct(self, normal):
        return sum(n*v for n,v in zip(normal, self.__velocity))

    def draw(self):
        self.__ball.reparentTo(self.__gameEngine.render)

    def update(self, elapsedTime):
        if self.__velocity[0] == 0:
            self.__velocity[0] += 3
            self.__velocity[1] -= self.__velocity[1]/abs(self.__velocity[1])*3
        elif self.__velocity[1] == 0:
            self.__velocity[1] += 3
            self.__velocity[0] -= self.__velocity[0]/abs(self.__velocity[0])*3
        if self.__velocity[0] in range(-2, 2):
            self.__velocity[0] += self.__velocity[0]/abs(self.__velocity[0])*2
            self.__velocity[1] -= self.__velocity[1]/abs(self.__velocity[1])*2
        elif self.__velocity[1] in range(-2, 2):
            self.__velocity[1] += self.__velocity[1]/abs(self.__velocity[1])*2
            self.__velocity[0] -= self.__velocity[0]/abs(self.__velocity[0])*2
        moveVector = self.__velocity*elapsedTime
        self.__position = self.__ball.getPos() + moveVector
        self.__ball.setFluidPos(self.__position)

    def destroy(self):
        self.__ball.removeNode()
        #self.__wallCollider.removeNode()
