#geometry.py, base class for all geometry

import numpy as np

from material import *
from ray import *



class Geometry(Material):
    """A base class for geometry"""

    # Constructor Geometry
    def __init__(self, Material):
        self.Material = Material
        self.name = "Noname"

    def setPosition(self, x, y, z):
        self.position = np.array([x, y, z])

    def getPosition(self):
        return self.position

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getNormal(self, surfacePoint):
        pass

    def intersect(self, r):
        pass
