# -*- coding:utf-8 -*-

from math import sqrt, cos, sin, asin, atan, pi

class Vector (object):

    '''
    Classe modélisant un vecteur du plan.
    '''

    #Précision : 10 décimales après le 0
    DEC_PRECISION = 10

    def __init__(self, *args):
        self.refresh(*args)
        #L'unité S.I.
        self.unit = "(no unit)"

    def refresh(self, *args):
        ''' Actualise un vecteur. args contient soit les composantes en x et y, soit la norme, la dir. et le sens '''

        assert 2 <= len(args) <= 3

        try:
            #Cas où on fournit les composantes
            if len(args) == 2:
                #Composantes
                self.x = float(args[0])
                self.y = float(args[1])

                #Norme
                self.val = sqrt(self.getX()*self.getX() + self.getY()*self.getY())

                #Direction
                self.dir_rad = abs( asin(self.getY() / self.getVal()) )
                self.dir_deg = Vector.radToDeg(self.dir_rad)

                #Sens
                sign = lambda b : False if b<0 else True
                self.sense = ( sign(self.getX()), sign(self.getY()) )

            #Cas où on fournit la norme, la dir. et le sens
            else:
                #Norme
                self.val = args[0]

                #Direction (degrés en arg.)
                self.dir_deg = float(args[1])
                self.dir_rad = Vector.degToRad(self.dir_deg)

                #Sens
                #True : Positif, False : Negatif
                #Tableau t.q. sense[0] -> sens x et sense[1] -> sens y
                self.sense = args[2]

                #Composantes : valeur absolue
                self.x = self.getVal() * cos(self.getDir()[1])
                self.y = self.getVal() * sin(self.getDir()[1])

                #Composantes : valeur signée
                sign = lambda b : (-1) if b==False else (1)
                self.x *= sign(self.getSense()[0])
                self.y *= sign(self.getSense()[1])

            values = (self.getX(), self.getY(), self.getVal(), self.getDir()[0], self.getDir()[1])
            values = tuple( round(value, Vector.DEC_PRECISION) for value in values )
            self.x, self.y, self.val, self.dir_deg, self.dir_rad = values 

        except (ZeroDivisionError, TypeError):
            self.x = 0
            self.y = 0
            self.val = 0
            self.dir_deg = None
            self.dir_rad = None
            self.sense = None

    #---------------------------------------------------------------------------------------------------------------------------------------#
    #                                                           Surcharge d'opérateur                                                       #
    #---------------------------------------------------------------------------------------------------------------------------------------#

    def __add__(self, vect):
        x = self.getX() + vect.getX()
        y = self.getY() + vect.getY()
        return self.opOverload(x,y)

    def __sub__(self, vect):
        x = self.getX() - vect.getX()
        y = self.getY() - vect.getY()
        return self.opOverload(x,y)

    def __mul__(self, num):
        ''' Produit d'un vecteur avec un nombre '''
        x = self.getX()*num
        y = self.getY()*num
        return self.opOverload(x,y)

    def __rmul__(self, num):
        ''' Pareil que __mul__ '''
        return self.__mul__(num)

    def __div__(self, num):
        ''' Division d'un vecteur par un nombre '''
        return self*(1/num)

    def __rdiv__(self, num):
        return self.__div__(num)

    def opOverload(self, *args):
        ''' A redéfinir par une classe fille pour définir le type de l'objet renvoyé '''
        return Vector(*args)

    #---------------------------------------------------------------------------------------------------------------------------------------#
    #                                                                         Calculs                                                       #
    #---------------------------------------------------------------------------------------------------------------------------------------#
 
    @staticmethod
    def degToRad(deg):
        return deg*pi/180

    @staticmethod
    def radToDeg(rad):
        return 180*rad/pi

    @staticmethod
    def calcDir(a, b):
        ''' Calcule la direction entre deux points, en ° '''

        deltax = abs(a[0]-b[0])
        deltay = abs(a[1]-b[1])

        try:
            #Le coef directeur est m=delta_y/delta_x, avec un peu de trigo on trouve que l'angle vaut tan(m)
            return Vector.radToDeg(atan( float(deltay)/deltax ))

        except ZeroDivisionError:
            #La direction est d'équation x=... au lieu de y=... (constante, // à (Oy))
            return Vector.degToRad(90)

    @staticmethod
    def calcSense(a, b):
        ''' Calcule le sens (de a vers b) '''
        sense = lambda a, b : True if a<b else False
        return (sense(a[0], b[0]), sense(a[1], b[1]))

    #---------------------------------------------------------------------------------------------------------------------------------------#
    #                                                                      Getters                                                          #
    #---------------------------------------------------------------------------------------------------------------------------------------#
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getVal(self):
        return self.val

    def getDir(self):
        return (self.dir_deg, self.dir_rad)

    def getSense(self):
        return self.sense

    def getUnit(self):
        return self.unit

#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                Types spéciaux de vecteurs                                             #
#---------------------------------------------------------------------------------------------------------------------------------------#

class Force (Vector):

    def __init__(self, *args):

        #Si on fournit l'intensité et deux points
        if len(args) == 3:
            intensity = args[0]
            assert intensity >= 0

            if intensity == 0:
                super(Force, self).__init__(intensity, None, (None, None))

            else:
                a = args[1]
                b = args[2]

                #Force d'attraction, donc Fa/b => de b vers a
                super(Force, self).__init__(intensity, Vector.calcDir(b,a), Vector.calcSense(b,a))

        else:
            super(Force, self).__init__(*args)

    def opOverload(self, *args):
        return Force(*args)

class Acceleration (Vector):

    def __init__(self, *args):
        super(Acceleration, self).__init__(*args)
        self.unit = "m/s²"

    def opOverload(self, *args):
        return Acceleration(*args)

class Speed (Vector):

    def __init__(self, *args):
        super(Speed, self).__init__(*args)
        self.unit = "m/s"

    def opOverload(self, *args):
        return Speed(*args)
