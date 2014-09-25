#geometry.py, base class for all geometry

import numpy as np

from material import Material
from ray import Ray



class Geometry(Material):
    """A base class for geometry"""

    #constructor
    def __init__(self):
        super(Material, self).__init__()

    def setPosition(self, x, y, z):
        self.position(np.array([x,y,z]))

    def getPosition(self):
        return self.position

    def intersect(r):
        pass
