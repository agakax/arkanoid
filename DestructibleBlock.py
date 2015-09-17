__author__ = 'Kamil'

from Block import Block

class DestructibleBlock(Block):
    def __init__(self, gameEngine, position):
        Block.__init__(self, gameEngine)
        self._durability = 1
        self._points = 10
        self.loadModel('models/cube_wa3')
        self.setModelTexture('textures/bricks.jpg')
        self.setModelParameters(position)
        self.createHitCollider()
        self.createCeilCollider()
        self.createFloorCollider()
        self.createRay()
        self.setFallCollideHandling()

    def ballHit(self):
        self._durability -= 1
        if self._durability == 0:
            pass


