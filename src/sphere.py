    #Sphere.py

import numpy as np

from numpy import linalg as LA
from numpy import multiply as vecMult

from geometry import Geometry
from ray import Ray
from material import Material


class Sphere(Geometry):
    """A class for sphere objects
    radius: Sphere's radius
    """

    #constructor
    def __init__(self, material=Material(), radius=1):
        super(Sphere, self).__init__(material)
        self.radius = radius


    #================================================================
    #========================== SETTERS =============================
    #================================================================

    #Set radius
    def setRadius(self, radius):
        self.radius = radius

    #Set center point
    def setCenterPoint(self, c):
        self.centerPoint = c

    #================================================================
    #========================== GETTERS =============================
    #================================================================

    #Get radius
    def getRadius(self):
        return self.radius

    #Get center point
    def getCenterPoint(self):
        return self.centerPoint

    #Get surface normal in point
    def getNormal(self, surfacePoint):
        direction = np.subtract(surfacePoint, self.centerPoint)
        # u = u/||u||
        directionNorm = 1/LA.norm(direction)
        normal = np.multiply(direction, directionNorm)
        return normal



    #================================================================
    #========================= VIRTUALS (Override) ==================
    #================================================================

    #Intersect sphere
    def intersect(self, r):
        """
        Looks for intersections with a sphere for a ray
        :param r: Ray object which includes an origin point and a direction
        :return: False when ray has no intersection or tangent to the sphere, Returns intersection point as np.array if there is an intersection
        """

        if isinstance(r, Ray) is True:
            #Check if ray really intersect with the sphere, i.e. has 2 insection points. Otherwise do not calculate the roots.
            #Ray : P = P0 + t*V
            #Sphere: |P-O|^2 = r^2 => ... => |P0 + t*V - O|^2 - r^2 = 0
            # Gives a quadratic equation at^2 + bt + c = 0
            # => ... => a = ||V||^2, b = 2*V(P0 - O), c = ||P0 - O||^2 - r^2
            # Will result in t = -b/2 +- sqrt((b/2)^2 - c) = -V(P0 - O +- sqrt((V(P0 - O))^2 - c)
            a = 1 # since V is a unit vector => a = ||V||^2 = 1
            b = 2 * np.dot(r.direction, r.origin - self.centerPoint)
            c = LA.norm(r.origin - self.centerPoint)**2 - self.radius**2 #(**2 = ^2)
            underSqrt = (b/2)**2 - a*c

            if underSqrt < 0:
                # No intersection, will not be any real roots
                return -1
            elif underSqrt == 0:
                # One intersection (tangent), only one solution but is neglected in this case
                return -1
            else:
                #Intersection with sphere!
                squareroot = underSqrt**0.5
                #We only want to know the intersection point closest to the camera; so select the lowest solution
                t = -(b/2)/a - squareroot
                
                #intersection = t*vecMult(t, r.direction)
                #return intersection
                return t
