__author__ = 'Kamil'

from Block import Block

class DestructibleBlock(Block):
    def __init__(self, gameEngine, position, blockId):
        Block.__init__(self, gameEngine, blockId)
        self._durability = 1
        self._points = 10
        self.loadModel('models/cube_new')
        self.setModelTexture('textures/bricks.jpg')
        self.setModelParameters(position)
        self.createHitCollider(blockId)
        self.createCeilCollider(blockId)
        self.createRay(blockId)
        self.setFallCollideHandling()

    def ballHit(self):
        self._durability -= 1
        if self._durability == 0:
            self.destroy()

