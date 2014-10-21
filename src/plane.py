#!/usr/bin/python
# coding: utf-8
#plane.py, Class for plane objects

import numpy as np
import random as rand

from geometry import *
from ray import *
from material import *

class Plane(Geometry):

	# Constructor
    def __init__(self, material=Material()):
        super(Plane, self).__init__(material)

    #================================================================
    #========================== SETTERS =============================
    #================================================================

    def setNormal(self, normalX, normalY, normalZ):
    	self.normal = np.array([normalX, normalY, normalZ])

    def setPointSouthWest(self, x, y, z):
    	self.pointSouthWest = np.array([x, y, z])
        self.setPosition(x, y, z)

    def setPointNorthWest(self, x, y, z):
        self.pointNorthWest = np.array([x, y, z])

    def setPointNorthEast(self, x, y, z):
        self.pointNorthEast = np.array([x, y, z])

    def setPointSouthEast(self, x, y, z):
        self.pointSouthEast = np.array([x, y, z])

    def __setPosition(self, x, y, z):
    	super(Plane, self).setPosition(x, y, z)


    #================================================================
    #========================== GETTERS =============================
    #================================================================

    def getNormal(self, surfacePoint):
    	return self.normal

    def getRandomPoint(self):
        vec1 = self.pointNorthWest - self.pointSouthWest
        vec2 = self.pointSouthEast - self.pointSouthWest
        vec1 = vec1 * rand.random()
        vec2 = vec2 * rand.random()
        return self.pointSouthWest + vec1 + vec2


    #================================================================
    #========================= VIRTUALS (Override) ==================
    #================================================================

    #Intersect sphere
    def intersect(self, r):
        if isinstance(r, Ray) is True:

            EPSILON = 0.000001
            denom = np.dot(self.normal, r.direction)

            if denom < -EPSILON:
                originToCenter = self.position - r.origin
                t = np.dot(originToCenter, self.normal) / denom
                if t > 0:
                    #return t
                    
                    p = r.origin + r.direction * t                   
                    vec1 = self.pointNorthWest - self.pointSouthWest
                    vec2 = self.pointSouthEast - self.pointSouthWest
                    x = np.dot((p - self.pointSouthWest), vec1) / np.dot(vec1, vec1)
                    y = np.dot((p - self.pointSouthWest), vec2) / np.dot(vec2, vec2)

                    if 0.0 <= x <= 1.0 and 0.0 <= y <= 1.0: 
                        return t
            return -1


