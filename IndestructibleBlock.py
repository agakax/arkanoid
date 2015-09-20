__author__ = 'Kamil'

from Block import Block

class IndestructibleBlock(Block):
    def __init__(self, gameEngine, position, blockId):
        Block.__init__(self, gameEngine)
        self._durability = -1
        self._points = 0
        self.loadModel('models/cone_wo2')
        self.setModelTexture('textures/bricks.jpg')
        self.setModelParameters(position)
        self.createHitCollider(blockId)
        self.createRay()
        self.setFallCollideHandling()

    def ballHit(self):
        pass