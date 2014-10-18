#!/usr/bin/python
# coding: utf-8
#tracer.py, Class for the actual Ray Tracer

import numpy as np
import random as rand

from OpenGL.GL import *
from OpenGL.GLUT import *
from scene import *
from ray import *

class Tracer():
        # Constructor Tracer
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.Scene = Scene(np.array([75.0, 50.0, 250.0]), 45.0, (width / height))

        # Init Tracer
        def init(self):
            self.Scene.setupScene()

        def startRayTrace(self, pixelPosX, pixelPosY):
             # Calculate ray origin and direction by pixel position
            rayDirection = np.array([0.0, 0.0, 0.0])
            rayOrigin = np.array([0.0, 0.0, 0.0])
            rayOrigin[0] = (pixelPosX / self.width) * (2 * self.Scene.cameraPos[0])
            rayOrigin[1] = (pixelPosY / self.height) * (2 * self.Scene.cameraPos[1])
            rayOrigin[2] = self.Scene.cameraPos[2] - ((1 / (np.tan(self.Scene.fovY/2))) * self.Scene.cameraPos[0])
            rayDirection = rayOrigin - self.Scene.cameraPos
            rayDirection = rayDirection / np.linalg.norm(rayDirection)

             # Spawn new ray
            ray = Ray(rayDirection, rayOrigin)

            #Start recursive ray trace
            return self.traceRay(ray, 1)

        def traceRay(self, ray, iteration):
            if isinstance(ray, Ray) is False:
                return None



            # Russian Roulette random variable
            rr = rand.random()

            # Pixel Color
            pixelColor = [0.0, 0.0, 0.0, 1.0]

            # Check first intersection
            tClose = 9999

            # Go through all geometry in the scene
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                matColor = geometry[g].Material.getColor()
                t = geometry[g].intersect(ray)
                if t > 0 and t < tClose:
                    tClose = t
                    pixelColor =  [matColor[0], matColor[1], matColor[2], 1.0]
                    firstGeometry = geometry[g]

            if tClose>=9999:
                return pixelColor

            #Exceeded number of iterations, return closest intersected material color
            if iteration >20:
                matColor = firstGeometry.Material.getColor()
                pixelColor =  [matColor[0], matColor[1], matColor[2], 1.0]
                return pixelColor 

            if (firstGeometry.Material.getLight()):
                return pixelColor

            #Intersection with closest geometry, get material properties and calculate new direction for recursive call
            if(tClose<9999 and tClose>0.0001):

                reflection = firstGeometry.Material.getReflection()
                refraction = firstGeometry.Material.getRefraction()

                intersectionPoint = ray.origin + ray.direction * tClose
                intersectionNormal = firstGeometry.getNormal(intersectionPoint)

                #new ray direction & origin point
                ray.direction = intersectionNormal
                ray.origin = intersectionPoint

                return (np.multiply(pixelColor, 0.9) + np.multiply(self.traceRay(ray, iteration+1),0.1))
