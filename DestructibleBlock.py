__author__ = 'Kamil'

from Block import Block

class DestructibleBlock(Block):
    def __init__(self, gameEngine, position, blockId):
        Block.__init__(self, gameEngine, str(blockId))
        self._durability = 1
        self._points = 10
        self.loadModel('models/cube_wa3')
        self.setModelTexture('textures/bricks.jpg')
        self.setModelParameters(position)
        self.createHitCollider('block' + str(blockId))
        self.createFloorSensor('block' + str(blockId))
        self.createRayCollider('block' + str(blockId))

    def ballHit(self):
        self._durability -= 1


