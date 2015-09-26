__author__ = 'Kamil'

from os import listdir
from os.path import isfile, join
from panda3d.core import LPoint3f
import re
from Block import Block
from DestructibleBlock import DestructibleBlock
from IndestructibleBlock import IndestructibleBlock

class LevelBlocks(object):
    __gameEngine = None
    __base = None
    __level = 0
    __levelsFiles = []
    __blocks = []

    def __init__(self, gameEngine, base):
        self.__base = base
        self.__gameEngine = gameEngine
        self.getLevelsList()
        self.defineCollisionEventHandling()

    def getLevelsList(self):
        self.__levelsFiles = [ file for file in listdir('levels/') if isfile(join('levels/', file))]

    def loadLevelBlocks(self):
        levelFile = open('levels/' + self.__levelsFiles[self.__level], 'r')
        x = 0
        y = 0
        z = 0
        blockId = 0
        for line in levelFile:
            if line.strip():
                line = line.strip()
                row = line.split(',')
                for el in row:
                    pos = self.computePosition(x, y, z)
                    block = self.createBlock(el, pos, blockId)
                    if block != None:
                        self.__blocks.append(block)
                        blockId += 1
                    x += 1
                x = 0
                y += 1
            else:
                x = 0
                y = 0
                z += 1

    def computePosition(self, x, y, z):
        startPos = LPoint3f(10, 65, 10)
        multiplier = Block.SCALE * 2
        return LPoint3f(startPos[0] + (x*multiplier), startPos[1] - (y*multiplier), startPos[2] + (z*multiplier))

    def createBlock(self, element, position, blockId):
        if element == '1':
            return DestructibleBlock(self.__gameEngine, self.__base, position, blockId)
        elif element == '2':
            return IndestructibleBlock(self.__gameEngine, self.__base, position, blockId)
        else:
            return None

    def defineCollisionEventHandling(self):
        self.__gameEngine.accept('hitBlock', self.ballHitBlock)

    def ballHitBlock(self, entry):
        blockName = entry.getIntoNodePath().getName()
        blockId = int(re.findall(r'\d+', blockName)[0])
        self.__blocks[blockId].ballHit()

    def draw(self):
        for block in self.__blocks:
            block.draw()

    def update(self, elapsedTime):
        pass

    def destroy(self):
        for block in self.__blocks:
            block.destroy()
        del self.__blocks[:]
        self.__levelsFiles = []