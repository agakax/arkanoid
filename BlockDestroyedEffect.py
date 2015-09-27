__author__ = 'Kamila'
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import Filename, LVecBase3f

class BlockDestroyedEffect(object):
    __base = None
    __pos = None
    def __init__(self, base, pos):
        self.__base = base
        self.__pos = pos
        self.particleEffect()

    def particleEffect(self):
        self.p = ParticleEffect()
        self.loadParticleConfig('particleEffect.ptf')
        self.__base.taskMgr.doMethodLater(0.5, self.cleanUpParticles, "cleanup")

    def cleanUpParticles(self, task):
         self.p.softStop()

    def loadParticleConfig(self, file):
        self.p.cleanup()
        self.p = ParticleEffect()
        self.p.loadConfig(Filename(file))
        self.p.setPos(self.__pos.x, self.__pos.y, 2)
        self.p.start(parent = self.__base.render, renderParent = self.__base.render)