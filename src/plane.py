#!/usr/bin/python
# coding: utf-8
#plane.py, Class for plane objects

import numpy as np

from geometry import Geometry
from ray import Ray

class Plane(Geometry):

	#constructor
    def __init__(self, normalX, normalY, normalZ, width, height):
        super(Geometry, self).__init__()
        self.normal = np.array([normalX, normalY, normalZ])
        self.width
        self.height


    def getCenter(self):