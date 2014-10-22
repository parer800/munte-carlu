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
            self.MAX_DISTANCE = 999
            self.width = width
            self.height = height
            self.Scene = Scene(np.array([75.0, 50.0, 250.0]), 45.0, (width / height))

        # Init Tracer
        def init(self):
            self.Scene.setupScene()

        def startRayTrace(self, pixelPosX, pixelPosY, importance):
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
            return self.traceRay(ray, 1, importance)

        def traceRay(self, ray, iteration, importance):


            # IF number of iterations > Maxiterations OR importance < minimiimportance
            if iteration > 20 or importance < 0.0001:
                return [0.0, 0.0, 0.0, 1.0]


            # Check intersection point of closest geometry
            tClose = 999999
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                t = geometry[g].intersect(ray)
                if t > -1 and t < tClose:
                    tClose = t
                    firstGeometry = geometry[g]

            # IF geometry is light then return light color
            if firstGeometry.Material.getLight() == True: 
                lightColor = firstGeometry.Material.getColor()
                return [lightColor[0], lightColor[1], lightColor[2], 1.0]


            # IF intersection point > max distance
            if tClose > self.MAX_DISTANCE:
                return [0.0, 0.0, 0.0, 1.0]


            accPixelValue = [0.0, 0.0, 0.0]
            # IF reflective or refractive object
            # PUT SOME CODE HERE FOR THAT! RETURN accPixelValue
            if firstGeometry.Material.getLight() == False and firstGeometry.Material.getWall() == False:
                test = 1

            # ELSE IF diffuse lambertian BRDF
            # PUT SOME CODE HERE FOR THAT! RETURN accPixelValue
            # Monte-Carlo BRDF
            elif firstGeometry.Material.getWall() == True and firstGeometry.getName() == 'WallBack':
                rr = rand.random()
                if rr < 0.5: # STATIC VALUE KAN ÄNDRAS TILL ANNAT VÄRDE
                    intersectionPoint = ray.origin + ray.direction * tClose
                    newRay = self.calculateDiffuseRay(intersectionPoint, firstGeometry.getNormal(intersectionPoint))
                    accPixelValue = self.traceRay(newRay, iteration+1, importance)


            # Calculate shadow ray            
            intersectionPoint = ray.origin + ray.direction * tClose
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                 if geometry[g].Material.getLight() == True:
                    lightPoint = geometry[g].getRandomPoint()
                    lightVec = lightPoint - intersectionPoint
                    
                    if self.calculateShadow(intersectionPoint, lightVec):
                        return [0.0, 0.0, 0.0, 1.0]
            


            # Calculate direct light with Phong Shading Model
            #return [1.0, 0.0, 0.0, 1.0]
            return accPixelValue + self.calculateDirectLight(intersectionPoint, firstGeometry, ray)


            # Return value
            # return (accPixelValue + objectColor + lambert * lambert * shade * phong * diffuse * lightColor)


        def calculateDiffuseRay(self, intersectionPoint, pointNormal):

            r1 = rand.random()
            r2 = rand.random()
            phi = 2 * np.pi * r1
            theta = np.arccos(np.sqrt(r2))

            # To cartesian coordinates
            x = np.cos(phi) * np.sin(theta)
            y = np.sin(phi) * np.sin(theta)
            z = np.cos(theta)

            randomRay = Ray([x, y, z], intersectionPoint)

            return randomRay

        def calculateDirectLight(self, intersectionPoint, geometryObject, ray):
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                if (geometry[g].Material.getLight()):
                    lightPoint = geometry[g].getRandomPoint()
                    lightVec =   lightPoint - intersectionPoint

                    lightDistance = np.linalg.norm(lightVec)
                    lightVecNormalized = lightVec / lightDistance
                    lightColor = geometry[g].Material.getColor()
                    lightRadiance = geometry[g].Material.getRadiance()
                    lightDistance = lightDistance * lightDistance

                    geometryObjectNormal = geometryObject.getNormal(intersectionPoint)
                    geometryObjectColor = geometryObject.Material.getColor()
                    geometryObjectDiffuse = geometryObject.Material.getDiffuse()
                    geometryObjectSpecular = geometryObject.Material.getSpecular()
                    geometryObjectSpecularPower = geometryObject.Material.getSpecularPower()

                    # Diffuse Color
                    NdotL = np.dot(geometryObjectNormal, lightVecNormalized)
                    diffuse = np.clip(NdotL, 0, 1) * geometryObjectDiffuse

                    # Half Vector
                    halfVector = lightVecNormalized + ray.direction
                    halfVector = halfVector / np.linalg.norm(halfVector)

                    # Specular Color
                    NdotH = np.dot(geometryObjectNormal, halfVector)
                    specular = np.power(np.clip(NdotH, 0, 1), geometryObjectSpecularPower) * geometryObjectSpecular

                    # Shade
                    #shade = (1 / np.linalg.norm(lightVec))

                    return (geometryObjectColor * diffuse + specular) * lightColor

        def calculateShadow(self, intersectionPoint, lightVec):
            shadowRay = Ray(lightVec / np.linalg.norm(lightVec), intersectionPoint)
            
            tClose = 999999
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                if geometry[g].Material.getLight() == False and geometry[g].Material.getTransparency() == False:
                    t = geometry[g].intersect(shadowRay)
                    if t > -1 and t < tClose:
                        tClose = t

            if tClose < self.MAX_DISTANCE:
                shadowRayIntersectionPoint = shadowRay.origin + shadowRay.direction * tClose
                shadowRayIntersectionLength = np.linalg.norm(shadowRayIntersectionPoint - intersectionPoint)
                if shadowRayIntersectionLength < np.linalg.norm(lightVec):
                    return True



            return False






        '''
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

        if tClose >= 9999:
            return pixelColor

        intersectionPoint = ray.origin + ray.direction * tClose
        if self.calculateDirectLight(None, intersectionPoint):
            return [0, 0, 0, 1.0]

        matColor = firstGeometry.Material.getColor()
        pixelColor = [matColor[0], matColor[1], matColor[2], 1.0]
        return pixelColor
        '''
        '''
        #Exceeded number of iterations, return closest intersected material color
        if iteration >20:
            matColor = firstGeometry.Material.getColor()
            pixelColor = [matColor[0], matColor[1], matColor[2], 1.0]
            return pixelColor 

        if (firstGeometry.Material.getLight()):
            return pixelColor
        '''

        '''
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
        '''
