# -*- coding:utf-8 -*-

from vectors import *
from time import time

class Particle (object):

        '''
        Représente une particule avec sa masse, sa position dans un plan, sa vitesse, son accélération, sa force résultante extérieure.
        '''

        G = 6.67e-11

	#Valeurs par défaut
	DEF_MASS = 1e14
	DEF_FORCE = Force(0,0) 
	DEF_V = Speed(0,0)
	DEF_A = Acceleration(0,0)

	collisions = True

	def __init__(self, pos, mass=DEF_MASS, f=DEF_FORCE, v=DEF_V, a=DEF_A):

		#Données physiques
		self.pos = pos
		self.mass = mass
		self.radius = mass*1e-13
		self.f = f
		self.v = v
		self.a = a

		#Instant t=t(n-1), n étant l'instant actuel
		self.t_before = time()
		
		#Etat de la particule
		self.killed = False

	def update(self, other_particles):
                ''' S'occupe de MAJ les caractéristiques de la particule depuis le dernier appel de la fonction '''
		#Force résultante
		self.f = Force(0,0)

		for p in other_particles:
			f = Particle.calcGravForce(p, self)
			self.f += f

		self.a = Particle.calcAcc(self)

		t_now = time()
		self.v = Particle.calcSpeed(self, t_now-self.t_before)
		self.pos = ( self.getPos()[0] + self.getSpeed().getX(), self.getPos()[1] + self.getSpeed().getY() )

		self.t_before = t_now

	@staticmethod
	def check_collisions(particles):
		''' Donne naissance à une particule qd deux autres se collisionnent '''

		news = list()

		for i in range(len(particles)):
			for j in range(i+1, len(particles)):
				p_1 = particles[i]
				p_2 = particles[j]
				
				d = Particle.calcDist(p_2, p_1)

				if p_1.isAlive() and p_2.isAlive() and d <= p_1.getRadius()+p_2.getRadius():
					if p_1.getMass() >= p_2.getMass():
						news.append( p_1.collide(p_2) )
					else:
						news.append( p_2.collide(p_1) )
		return news

	def collide(self, particle):

		if Particle.collisions:
			#Masse
			m = self.getMass() + particle.getMass()

			#Moyenne pondérée des positions
			pos_x = (self.getMass()*self.getPos()[0] + particle.getMass()*particle.getPos()[0]) / m
			pos_y = (self.getMass()*self.getPos()[1] + particle.getMass()*particle.getPos()[1]) / m

			#Qté de mouvement
			#->    ->
			#p = m.v	      ->    ->			 ->   	 ->
			#p constante, donc ma.va+mb.vb = p, d'où v = (ma.va + mb.vb) / (ma+mb)
			v = (self.getSpeed()*self.getMass() + particle.getSpeed()*particle.getMass()) / (self.getMass()+particle.getMass())
			#Accélération nulle (pour l'instant)
			a = Acceleration(0, 0)
			#Force
			f = m*a

			self.kill()
			particle.kill()

			#Nvelle particule
			return Particle( (pos_x, pos_y), mass=m, f=f, v=v, a=a )

		else:
			p = Particle((0,0))
			p.kill()
			return p

	#---------------------------------------------------------------------------------------------------------------------------------------#
	#                                                               Calculs généraux							#
	#---------------------------------------------------------------------------------------------------------------------------------------#

        @staticmethod
        def calcDist(p_1, p_2):
                ''' Calcule la distance entre deux particules '''
                return sqrt( pow(p_1.getPos()[0] - p_2.getPos()[0], 2) + pow(p_1.getPos()[1] - p_2.getPos()[1], 2) )

        @staticmethod
        def calcGravForce(p_1, p_2):
                ''' Calcule l'interaction gravitationnelle entre deux particules '''
                d = Particle.calcDist(p_1, p_2)
                f = (Particle.G * p_1.getMass() * p_2.getMass()) / (d*d)
                return Force(f, p_1.getPos(), p_2.getPos())

        @staticmethod
        def calcSpeed(particle, time_diff):
                ''' Calcule la vitesse d'une particule '''
                #->       ->                ->
                #v(t=t1) = v(t=t0) + (t1-t0).a(t=t0)
                return particle.getSpeed() + time_diff*particle.getAcc()

        @staticmethod
        def calcAcc(particle):
                ''' Calcule l'accélération d'une particule '''
                #->   ->
                #F = m.a
                return Acceleration(particle.getForce().getX(), particle.getForce().getY()) / particle.getMass()


	#---------------------------------------------------------------------------------------------------------------------------------------#
	#								Getters/Setters								#
	#---------------------------------------------------------------------------------------------------------------------------------------#

	def kill(self):
		self.killed = True

	def isAlive(self):
		return not self.killed

	def getPos(self):
		return self.pos

	def getMass(self):
		return self.mass

	def getRadius(self):
		return self.radius

	def getForce(self):
		return self.f

	def getSpeed(self):
		return self.v

	def getAcc(self):
		return self.a

	@staticmethod
	def collisionsMode():
		Particle.collisions = True

	@staticmethod
	def noCollisionsMode():
		Particle.collisions = False

class BlackHole (Particle):

	def __init__(self, pos, mass=Particle.DEF_MASS, f=Particle.DEF_FORCE, v=Particle.DEF_V, a=Particle.DEF_A):
		super(BlackHole, self).__init__(pos, mass, f, v, a)
		self.mass = Particle.DEF_MASS*1e3
		self.update( () )

	def update(self, *args):
		#Pour une question pratique... bien évidemment les trous noirs ont une dimension nulle
		self.radius = 50

	def collide(self, particle):
		if Particle.collisions:

			self.mass += particle.getMass()
			self.update( () )
			particle.kill()
			return particle

		else:
			return super(BlackHole, self).collide(particle)
