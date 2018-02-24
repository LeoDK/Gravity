# -*- coding:utf-8 -*-

import pygame, time
from pygame.locals import *
from physics import Particle, BlackHole
from copy import deepcopy
from math import cos, sin

class ColoredParticle (Particle):

    def __init__(self, pos, mass=Particle.DEF_MASS, 
                f=Particle.DEF_FORCE, 
                v=Particle.DEF_V, 
                a=Particle.DEF_A): 

        super(ColoredParticle, self).__init__(pos, mass=mass, f=f, v=v, a=a)
        self.update( () )

    def update(self, *args):
        super(ColoredParticle, self).update( *args )
        self.color = ColoredParticle.calcColor( self.getMass() )

    def collide(self, *args):
        p = super(ColoredParticle, self).collide( *args )

        if Particle.collisions:
            return ColoredParticle(p.getPos(), mass=p.getMass(), f=p.getForce(), v=p.getSpeed(), a=p.getAcc())
        else:
            return p

    @staticmethod
    def calcColor(mass):

        #Couleurs en fonction de la taille
        COLORS = (  (127, 255, 0),
                    (191, 255, 0),
                    (255, 255, 0),
                    (255, 191, 0),
                    (255, 127, 0),
                    (255, 0, 0),
                    (255, 0, 127),
                    (255, 0, 191),
                    (255, 255, 255) )

        q = int( mass/Particle.DEF_MASS )/2
        if q<1 : q = 1
        if q >= len(COLORS) : q = len(COLORS) -1

        return COLORS[q]

    def getColor(self):
        return self.color

class ColoredBlackHole (BlackHole, ColoredParticle):

    def __init__(self, pos, mass=ColoredParticle.DEF_MASS, 
                f=ColoredParticle.DEF_FORCE, 
                v=ColoredParticle.DEF_V, 
                a=ColoredParticle.DEF_A):

        ColoredParticle.__init__(self, pos, mass=mass, f=f, v=v, a=a)
        BlackHole.__init__(self, pos, mass=mass, f=f, v=v, a=a)

    def update(self, *args):
        BlackHole.update(self, *args)
        self.color = (0,0,0)

    def collide(self, *args):
        ret = BlackHole.collide(self, *args)
        self.update( () )
        return ret

class Window (object):

    SIZE_COEF = 9.0/10

    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.width = int( info.current_w*(Window.SIZE_COEF) )
        self.height = int( info.current_h*(Window.SIZE_COEF) )

        pygame.display.set_caption("Gravity simulation")
        self.screen = pygame.display.set_mode( (self.getWidth(), self.getHeight()) )
        self.particles = list()
        self.stopped = False

    def start(self):
        while self.isRunning():

            for event in pygame.event.get():

                if event.type == QUIT:
                    self.stop()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.particles.append( ColoredParticle(event.pos) )

                    elif event.button == 3:
                        self.particles.append( ColoredBlackHole(event.pos) )

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.reset()

                    elif event.key == K_c:
                        Particle.collisionsMode()

                    elif event.key == K_n:
                        Particle.noCollisionsMode()

            for i in range( len(self.getParticles()) ):
                save = deepcopy(self.getParticles())
                del self.particles[i]
                save[i].update(self.getParticles())
                self.particles = save

            news = Particle.check_collisions(self.getParticles())

            for p in self.getParticles():
                if p.getPos()[0] <= 0 or p.getPos()[0] >= self.getWidth() or p.getPos()[1] <= 0 or p.getPos()[1] >= self.getHeight():
                    p.kill()
                if p.isAlive():
                    news.append(p)

            self.particles = list()
            for n in news:
                if n.isAlive():
                    self.particles.append(n)

            self.screen.fill((20,20,20))

            for part in self.getParticles():
                Window.drawParticle(self.screen, part)

            pygame.display.update()

            time.sleep(0.05)

    @staticmethod
    def drawParticle(screen, particle):
        pos = map(int, particle.getPos())
        radius = int(particle.getRadius())

        pygame.draw.circle(screen, particle.getColor(), pos, radius, 0)

    def stop(self):
        self.stopped = True

    def reset(self):
        self.particles = []

    def isRunning(self):
        return not self.stopped

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getParticles(self):
        return self.particles
