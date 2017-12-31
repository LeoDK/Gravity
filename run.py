#!/home/leo/.virtualenvs/default/bin/python
# -*- coding:utf-8 -*-

from gui import Window
from time import sleep
from physics import *

print "******************************************************************************************"
print "*											*"
print "*				GRAVITY SIMULATOR					*"
print "*											*"
print "*	-Press C to enable collision mode						*"
print "*	-Press N to disable collision mode						*"
print "*	-Press SPACE to clear the screen						*"
print "*	-Left click to create lambda particle						*"
print "*	-Right click to create black hole						*"
print "*											*"
print "*Enjoy!											*"
print "******************************************************************************************"

sleep(2)

w = Window()

'''
#Mettre ici les actions à préfaire
w.particles.append( BlackHole((100, 200)) )
w.particles.append( BlackHole((500, 200)) )
w.particles.append( Particle((350, 400)) )
'''

w.start()
