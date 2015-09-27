__author__ = 'Kamil'

from Block import Block
from BlockDestroyedEffect import BlockDestroyedEffect

class DestructibleBlock(Block):
    def __init__(self, gameEngine, base, position, blockId):
        Block.__init__(self, gameEngine, base)
        self._durability = 1
        self._points = 10
        self.loadModel('models/cube_new')
        self.setModelTexture('textures/bricks.jpg')
        self.setModelParameters(position)
        self.createHitCollider(blockId)
        self.createCeilCollider()
        self.createRay()
        self.setFallCollideHandling()

    def ballHit(self):
        self._durability -= 1
        if self._durability == 0:
            BlockDestroyedEffect(self._base, self._block.getPos())
            self.destroy()

