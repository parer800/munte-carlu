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
        self.centerPoint = np.array(c)

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

            L = r.origin - self.centerPoint

            a = np.dot(r.direction, r.direction)
            b =  2*np.dot(r.direction, L)
            c = np.dot(L, L) - self.radius**2 #(**2 = ^2)

            disc = b*b - 4*a*c

            if disc < 0.0:
                # No intersection, will not be any real roots
                return -1

            distSqrt = np.sqrt(disc)
            if b < 0.0:
                q = (-b - distSqrt)/2
            else:
                q  = (-b + distSqrt)/2

            t0 = q/a
            #Can occur division with zero (q=0.0) when distance between ray.origin and center of sphere equals the radius of the sphere
            t1 = c/q


            if t0 > t1:
                temp = t0
                t0 = t1
                t1 = temp

            if t1 < 0.0:
                return -1

            if t0 < 0.0:
                t = t1
            else:
                t = t0
            return t

'''
#Test line sphere intersection, this result in a t of 3.15978504097, which seems to be correct
s = Sphere(Material(), 2.0)
s.setCenterPoint([5.0, 0.0, 0.0])
r = Ray([5.0, 0.0, 1.0], [0.0, 0.0, 0.0])
print s.intersect(r)
'''