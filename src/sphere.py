    #Sphere.py

import numpy as np


from geometry import Geometry
from ray import Ray

class Sphere(Geometry):
    """A class for sphere objects
    radius: Sphere's radius
    """

    #constructor
    def __init__(self, radius=1):
        super(Geometry, self).__init__()
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
    def intersect(r):
        if isinstance(r, Ray) is True:
            print r.direction