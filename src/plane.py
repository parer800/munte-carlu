#!/usr/bin/python
# coding: utf-8
#plane.py, Class for plane objects

import numpy as np

from geometry import *
from ray import *
from material import *

class Plane(Geometry):

	# Constructor
    def __init__(self, material=Material(), normalX=0.0, normalY=0.0, normalZ=1.0, width=50.0, height=50.0):
        super(Plane, self).__init__(material)
        self.normal = np.array([normalX, normalY, normalZ])
        self.width = width
        self.height = height


    #================================================================
    #========================== SETTERS =============================
    #================================================================

    def setNormal(self, normalX, normalY, normalZ):
    	self.normal = np.array([normalX, normalY, normalZ])

    def setWidth(self, width):
    	self.width = width

    def setHeight(self, height):
    	self.height = height

    def setPosition(self, x, y, z):
    	super(Plane, self).setPosition(x, y, z)


    #================================================================
    #========================== GETTERS =============================
    #================================================================

    def getNormal(self):
    	return self.normal

    def getWidth(self):
    	return width

    def getHeight(self):
    	return height


    #================================================================
    #========================= VIRTUALS (Override) ==================
    #================================================================

    #Intersect sphere
    def intersect(self, r):
        if isinstance(r, Ray) is True:

            denom = np.dot(self.normal, r.direction)

            if denom != 0:
                originToCenter = self.position - r.origin
                t = np.dot(originToCenter, self.normal) / denom
                if t >= 0:
                    return True

        	return False


