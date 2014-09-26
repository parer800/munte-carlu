    #Sphere.py

import numpy as np


from geometry import *
from ray import *
from material import *

class Sphere(Geometry):
    """A class for sphere objects
    radius: Sphere's radius
    """

    #constructor
    def __init__(self, material=Material(), radius=1):
        super(Geometry, self).__init__(material)
        self.radius = radius


    #================================================================
    #========================== SETTERS =============================
    #================================================================

    #Set radius
    def setRadius(self, radius):
        self.radius = radius

    #================================================================
    #========================== GETTERS =============================
    #================================================================

    #Get radius
    def getRadius(self):
        return self.radius


    #================================================================
    #========================= VIRTUALS (Override) ==================
    #================================================================

    #Intersect sphere
    def intersect(self, r):
        if isinstance(r, Ray) is True:
            #Check if ray really intersect with the sphere, i.e. has 2 insection points. Otherwise do not calculate the roots.
            #Ray : P = P0 + t*V
            #Sphere: |P-O|^2 = r^2 => ... => |P0 + t*V - O|^2 - r^2 = 0
            # Gives a quadratic equation at^2 + bt + c = 0
            # => ... => a = ||V||^2, b = 2*V(P0 - O), c = ||P0 - O||^2 - r^2
            # Will result in t = -b +- sqrt((b/2)^2 - c)
            b = 2 * np.dot(r.direction, r.origin)


            print r.direction