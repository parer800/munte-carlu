#!/usr/bin/python
# coding: utf-8
#tracer.py, Class for the actual Ray Tracer
from OpenGL.GL.NV import half_float
from OpenGLContext.resources import lights_vert_txt

import numpy as np
import random as rand
from numpy import linalg as LA


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
            return self.traceRay(ray, 1, importance, False)

        def traceRay(self, ray, iteration, importance, isInside):

            DIFFUSE_RAY_COUNT = 1
            SHADOW_RAY_COUNT = 2

            # IF number of iterations > Maxiterations OR importance < minimiimportance
            if iteration > 10:
                return [0.0, 0.0, 0.0, 1.0]


            # Check intersection point of closest geometry
            tClose = 999999
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                t = geometry[g].intersect(ray)
                if t > -1 and t < tClose:
                    tClose = t
                    firstGeometry = geometry[g]

            # IF intersection point > max distance
            if tClose > self.MAX_DISTANCE:
                return [0.0, 0.0, 0.0, 1.0]

            # IF geometry is light then return light color
            if firstGeometry.Material.getLight() == True:
                lightColor = firstGeometry.Material.getColor()
                intersectionPoint = ray.origin + ray.direction * tClose
                centerPoint = firstGeometry.getCenter()
                length = np.linalg.norm(np.subtract(intersectionPoint, centerPoint))
                factor = 1.0 + (length/100.0)
                return [lightColor[0]*factor, lightColor[1]*factor, lightColor[2]*factor, 1.0]

            tClose -= 0.01


            
            accPixelValue = [0.0, 0.0, 0.0, 1.0]

            # IF reflective or refractive object
            if firstGeometry.Material.getLight() is False and firstGeometry.Material.getWall() is False: 

                reflection = firstGeometry.Material.getReflection()
                refraction = firstGeometry.Material.getRefraction()
                intersectionPoint = ray.origin + ray.direction * tClose
                intersectionNormal = firstGeometry.getNormal(intersectionPoint)

                newRay = Ray(self.getSpecularRay(ray.direction, intersectionNormal, intersectionPoint), intersectionPoint)

                accPixelValue = self.traceRay(newRay, iteration+1, 1.0, False)
     



            # ELSE IF diffuse lambertian
            elif firstGeometry.Material.getWall() == True:
                rr = rand.random()
                if rr < np.power(firstGeometry.Material.getReflection(), iteration):
                    intersectionPoint = ray.origin + ray.direction * tClose
                    for d in range(DIFFUSE_RAY_COUNT):
                        
                        perfectReflection = np.subtract(ray.direction, np.multiply(np.multiply(2.0, np.dot(ray.direction, firstGeometry.getNormal(intersectionPoint))), firstGeometry.getNormal(intersectionPoint)))
                        perfectReflection = perfectReflection / LA.norm(perfectReflection)
                        newRay = self.calculateDiffuseRay(intersectionPoint, firstGeometry)
                        newImportance = ((firstGeometry.Material.getSpecularPower() + 2)/(2 * DIFFUSE_RAY_COUNT)) * np.power(np.dot(perfectReflection, newRay.direction), int(firstGeometry.Material.getSpecularPower()))
                        accPixelValue = np.add(accPixelValue, self.traceRay(newRay, iteration+1, newImportance, False))

                    accPixelValue[0] /= DIFFUSE_RAY_COUNT
                    accPixelValue[1] /= DIFFUSE_RAY_COUNT
                    accPixelValue[2] /= DIFFUSE_RAY_COUNT
                    accPixelValue[3] /= DIFFUSE_RAY_COUNT

            


            # Direct Light
            directLight = [0.0, 0.0, 0.0, 1.0]
            intersectionPoint = ray.origin + ray.direction * tClose
            eyeDirection =  self.Scene.cameraPos - intersectionPoint
            eyeDirection = eyeDirection / np.linalg.norm(eyeDirection)
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                 if geometry[g].Material.getLight() == True:
                    for s in range(SHADOW_RAY_COUNT):
                        directLight = np.add(directLight, self.calculateDirectLight(intersectionPoint, firstGeometry, ray, eyeDirection))
                     
                    directLight[0] /= SHADOW_RAY_COUNT
                    directLight[1] /= SHADOW_RAY_COUNT
                    directLight[2] /= SHADOW_RAY_COUNT
                    directLight[3] /= SHADOW_RAY_COUNT
                    break



            directColor = np.multiply(firstGeometry.Material.getDiffuse(), directLight)

            indirectColor = np.multiply((1.0 - firstGeometry.Material.getDiffuse()), np.multiply(importance, accPixelValue))
            totalColor = np.add(indirectColor, directColor)
            
            #print directColor
            #print indirectColor
            #print totalColor
            #print ' '

            #if firstGeometry.getName() == 'Roof':
            #    print totalColor
            
            return totalColor





        def getSpecularContribution(self, ray, object, iteration, importance):
                reflection = object.Material.getReflection()
                #Ireflection = importance*reflection
                materialColor = object.Material.getColor()
                materialColor = [materialColor[0], materialColor[1], materialColor[2], 1.0]
                #ray.origin = ray.origin + ray.direction * 10
                return (np.multiply(materialColor, 0.9) + np.multiply(self.traceRay(ray, iteration+1, 1.0, False),0.1))


        def getSpecularRay(self, newDirection, intersectNormal, intersectPoint):
            direction = newDirection
            directionNorm = 1/LA.norm(direction)
            direction = np.multiply(direction, directionNorm)
            newDir = np.subtract(direction, np.multiply(np.multiply(2.0, np.dot(direction, intersectNormal)), intersectNormal) )
            newDir = newDir / LA.norm(newDir)

            return newDir


        def getRefractedContribution(self, intersectionPoint, reflectedRay, geometryObject, ray, iteration, importance, isInside):
            Irefraction = 1 - importance
            normal = geometryObject.getNormal(intersectionPoint)
            if isInside is False:
                #outside n1 = 1.0
                n1 = 1.0
                n2 = geometryObject.Material.getIOR()
            else:
                #inside n1 = material's IOR
                n1 = geometryObject.Material.getIOR()
                n2 = 1.0
                normal = -normal



            NdotI = np.dot(normal, ray.direction)
          # print (1-((n1/n2)**2) * ((1 - NdotI)**2))
            component = -(n1/n2) * NdotI - (np.sqrt(1 - (((n1/n2)**2) * (1 - (NdotI)**2))))
            direction = (n1/n2) * reflectedRay + normal * component
            #print "n1 %f n2 %f" % (n1, n2)

            #Color of
            materialColor = geometryObject.Material.getColor()
            materialColor = [materialColor[0], materialColor[1], materialColor[2], 1.0]
            newRay = ray
            newRay.direction = direction
            ray.origin = ray.origin + 0.0001*ray.direction
            ray.direction = direction
            return (np.multiply(materialColor, importance) + np.multiply(self.traceRay(ray, iteration+1, Irefraction, True),0.1))


        def calculateDiffuseRay(self, intersectionPoint, firstGeometry):

            pointNormal = firstGeometry.getNormal(intersectionPoint)

            r1 = rand.random()
            r2 = rand.random()
            phi = 2 * np.pi * r1
            theta = np.arccos(np.sqrt(r2))

            # To cartesian coordinates
            x = np.cos(phi) * np.sin(theta)
            y = np.sin(phi) * np.sin(theta)
            z = np.cos(theta)
            newDirection = [x, y, z]

            # Rotate new direction to distribution of normal vector
            el = -1 * np.arccos(pointNormal[2])
            az = -1 * np.arctan2(pointNormal[1], pointNormal[0])
            rotationRay = [np.cos(el) * newDirection[0] - np.sin(el) * newDirection[2], newDirection[1], np.sin(el) * newDirection[0] + np.cos(el) * newDirection[2]]
            rotationRay = [np.cos(az) * rotationRay[0] + np.sin(az) * rotationRay[1], -1 * np.sin(az) * rotationRay[0] + np.cos(az) * rotationRay[1], rotationRay[2]]
            newDirectionCorrect = rotationRay / np.linalg.norm(rotationRay)

            randomRay = Ray(newDirectionCorrect, intersectionPoint)

            return randomRay

        def calculateDirectLight(self, intersectionPoint, geometryObject, ray, eyeDirection):
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                if (geometry[g].Material.getLight()):

                    lightPoint = geometry[g].getRandomPoint()
                    lightVec =   lightPoint - intersectionPoint

                    lightDistance = np.linalg.norm(lightVec)
                    lightVecNormalized = lightVec / lightDistance
                    lightColor = geometry[g].Material.getColor()
                    lightRadiance = geometry[g].Material.getRadiance()

                    constantAttenuation = 0.0001
                    linearAttenuation = 0.0001
                    quadraticAttenuation = 0.0001
                    addOnDistanceTerm = 1.0/(constantAttenuation + (linearAttenuation * lightDistance) + (quadraticAttenuation * lightDistance * lightDistance))

                    if addOnDistanceTerm > 1.0:
                        addOnDistanceTerm = 1.0

                    geometryObjectNormal = geometryObject.getNormal(intersectionPoint)
                    geometryObjectColor = geometryObject.Material.getColor()
                    geometryObjectDiffuse = geometryObject.Material.getDiffuse()
                    geometryObjectSpecular = geometryObject.Material.getSpecular()
                    geometryObjectSpecularPower = geometryObject.Material.getSpecularPower()

                    

                    # If shadow
                    if self.calculateShadow(intersectionPoint, lightVec) == True:
                        ambient = [0.1, 0.1, 0.1]
                        return [ambient[0], ambient[1], ambient[2], 1.0]

                    # Ambient Color
                    ambient = [0.7, 0.7, 0.7] * geometryObjectColor

                    # Diffuse Color
                    NdotL = np.dot(geometryObjectNormal, lightVecNormalized)
                    diffuse = np.clip(NdotL, 0, 1) * geometryObjectDiffuse * geometryObjectColor * lightColor

                    # Half Vector
                    halfVector = lightVecNormalized + eyeDirection
                    halfVector = halfVector / np.linalg.norm(halfVector)

                    if geometryObject.Material.getWall() == True:
                        color = (ambient + diffuse) * addOnDistanceTerm
                    else:
                        # Specular Color
                        NdotH = np.dot(halfVector, geometryObjectNormal)
                        specular = np.power(np.max(NdotH, 0), 4 * geometryObjectSpecularPower) * geometryObjectSpecular * geometryObjectColor * lightColor

                        color = (ambient + diffuse + specular) * addOnDistanceTerm

                    return [color[0], color[1], color[2], 1.0]



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



