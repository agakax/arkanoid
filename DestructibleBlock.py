__author__ = 'Kamil'

from Block import Block

class DestructibleBlock(Block):
    def __init__(self, gameEngine, position, blockId):
        Block.__init__(self, gameEngine)
        self._durability = 1
        self._points = 10
        self.loadModel('models/cube_wa3')
        self.setModelTexture('textures/bricks.jpg')
        self.setModelParameters(position)
        self.createCollider('block' + str(blockId) + 'CNode')

    def ballHit(self):
        self._durability -= 1


