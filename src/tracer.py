#!/usr/bin/python
# coding: utf-8
#tracer.py, Class for the actual Ray Tracer
from OpenGL.GL.NV import half_float
from OpenGLContext.resources import lights_vert_txt
import copy
import math
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
            
            #print ' '
            #print ' '
            #print ' '
            
            #Start recursive ray trace
            return self.traceRay(ray, 1, importance, False)

        def traceRay(self, ray, iteration, importance, isInside, depth=0, test='default'):

            DIFFUSE_RAY_COUNT = 1
            SHADOW_RAY_COUNT = 10
            MAX_ITERATION = 10
            MAX_DEPTH = 10

            if iteration > MAX_ITERATION or depth > MAX_DEPTH:
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

            
            
            accPixelValue =  [0.0, 0.0, 0.0, 1.0]

            # IF REFLECTIVE OR REFRACTIVE
            if firstGeometry.Material.getLight() is False and firstGeometry.Material.getWall() is False: 

                #Intersection point
                intersectionPointNormal = ray.origin + ray.direction * tClose
                intersectionNormal = firstGeometry.getNormal(intersectionPointNormal)

                intersectionPointRefracted = ray.origin + ray.direction * tClose
                intersectionPointReflected = ray.origin + ray.direction * tClose
                '''
                print depth
                print firstGeometry.getName()
                print test
                print isInside
                print tClose
                print importance
                print '-'
                '''
                # IF REFRACTIVE
                if firstGeometry.Material.getTransparency() is True:
                    
                    n1 = firstGeometry.Material.getIOR() if isInside else 1.0
                    n2 = 1.0 if isInside else firstGeometry.Material.getIOR()

                    # IF OUTSIDE OBJECT
                    if isInside is False:

                        refractionImportance = (((4 * n1 * n2) / ((n1 + n2) * (n1 + n2))) * importance)
                        reflectionImportance = (((n1 - n2) / (n1 + n2)) * ((n1 - n2) / (n1 + n2)) * importance)

                        reflectedRay = self.getSpecularRay(ray.direction, intersectionNormal, intersectionPointReflected)
                        reflectionColor = self.traceRay(reflectedRay, iteration+1, reflectionImportance, isInside, depth+1, 'reflection')
                        #accPixelValue =  np.add(accPixelValue, reflectionColor)
                        accPixelValue =  np.add(accPixelValue, np.multiply(reflectionImportance, reflectionColor))

                        refractedRay = self.getRefractedRay(ray.direction, intersectionNormal, intersectionPointRefracted, n1, n2)
                        if refractedRay != 0.0:
                            refractedColor = self.traceRay(refractedRay, iteration+1, refractionImportance, True, depth+1, 'refraction')
                            #accPixelValue =  np.add(accPixelValue, refractedColor)
                            accPixelValue =  np.add(accPixelValue, np.multiply(refractionImportance, refractedColor))

                    # IF INSIDE OBJECT
                    else:

                        # IF CRITICAL ANGLE
                        if np.arcsin(n2 / n1) > np.arccos(np.dot(-intersectionNormal, -ray.direction)):
                            
                            refractionImportance = (((4 * n1 * n2) / ((n1 + n2) * (n1 + n2))) * importance)
                            reflectionImportance = (((n1 - n2) / (n1 + n2)) * ((n1 - n2) / (n1 + n2)) * importance)

                            reflectedRay = self.getSpecularRay(ray.direction, -intersectionNormal, intersectionPointReflected)
                            reflectionColor = self.traceRay(reflectedRay, iteration+1, reflectionImportance, isInside, depth+1, 'reflection')
                            #accPixelValue =  np.add(accPixelValue, reflectionColor)
                            accPixelValue =  np.add(accPixelValue, np.multiply(reflectionImportance, reflectionColor))

                            refractedRay = self.getRefractedRay(ray.direction, -intersectionNormal, intersectionPointRefracted, n1, n2)
                            if refractedRay != 0.0:
                                refractedColor = self.traceRay(refractedRay, iteration+1, refractionImportance, False, depth+1, 'refraction')
                                #accPixelValue =  np.add(accPixelValue, refractedColor)
                                accPixelValue =  np.add(accPixelValue, np.multiply(refractionImportance, refractedColor))

                        # IF NO CRITICAL ANGLE
                        else:

                            reflectionImportance = importance

                            reflectedRay = self.getSpecularRay(ray.direction, -intersectionNormal, intersectionPointReflected)
                            reflectionColor = self.traceRay(reflectedRay, iteration+1, reflectionImportance, isInside, depth+1, 'reflection')
                            #accPixelValue =  np.add(accPixelValue, reflectionColor)
                            accPixelValue =  np.add(accPixelValue, np.multiply(reflectionImportance, reflectionColor))
                # IF REFLECTIVE
                else:

                    reflectionImportance = importance

                    reflectedRay = self.getSpecularRay(ray.direction, intersectionNormal, intersectionPointReflected)
                    reflectionColor = self.traceRay(reflectedRay, iteration+1, reflectionImportance, isInside, depth+1, 'reflection')
                    #accPixelValue =  np.add(accPixelValue, reflectionColor)
                    accPixelValue =  np.add(accPixelValue, np.multiply(reflectionImportance, reflectionColor))
        
            # ELSE IF DIFFUSE LAMBERTIAN
            elif firstGeometry.Material.getWall() == True:
                rr = rand.random()
                if rr < np.power(firstGeometry.Material.getReflection(), iteration):
                    intersectionPoint = ray.origin + ray.direction * (tClose - 0.01)
                    for d in range(DIFFUSE_RAY_COUNT):
                        
                        perfectReflection = np.subtract(ray.direction, np.multiply(np.multiply(2.0, np.dot(ray.direction, firstGeometry.getNormal(intersectionPoint))), firstGeometry.getNormal(intersectionPoint)))
                        perfectReflection = perfectReflection / LA.norm(perfectReflection)
                        newRay = self.calculateDiffuseRay(intersectionPoint, firstGeometry)
                        newImportance = ((firstGeometry.Material.getSpecularPower() + 2)/(2 * DIFFUSE_RAY_COUNT)) * np.power(np.dot(perfectReflection, newRay.direction), int(firstGeometry.Material.getSpecularPower()))
                    
                        accPixelValue = np.add(accPixelValue, self.traceRay(newRay, iteration+1, newImportance, False, depth))

                    accPixelValue[0] /= DIFFUSE_RAY_COUNT
                    accPixelValue[1] /= DIFFUSE_RAY_COUNT
                    accPixelValue[2] /= DIFFUSE_RAY_COUNT
                    accPixelValue[3] /= DIFFUSE_RAY_COUNT





            '''
            
            # IF REFLECTIVE OR REFRACTIVE
            if firstGeometry.Material.getLight() is False and firstGeometry.Material.getWall() is False: 

                #Intersection point
                intersectionPointNormal = ray.origin + ray.direction * tClose
                intersectionNormal = firstGeometry.getNormal(intersectionPointNormal)

                intersectionPointRefracted = ray.origin + ray.direction
                intersectionPointReflected = ray.origin + ray.direction

                # Reflection importance for opaque object
                reflectionImportance = importance

                # IF REFRACTIVE
                if firstGeometry.Material.getTransparency() is True:

                    n1 = firstGeometry.Material.getIOR() if isInside else 1.0
                    n2 = 1.0 if isInside else firstGeometry.Material.getIOR()

                    # Refraction and Reflection importance for transparent objects
                    refractionImportance = (((4 * n1 * n2) / ((n1 + n2) * (n1 + n2))) * importance)
                    reflectionImportance = (((n1 - n2) / (n1 + n2)) * ((n1 - n2) / (n1 + n2)) * importance)
                    
                    print isInside
                    print tClose
                    print importance
                    print refractionImportance
                    print reflectionImportance
                    print '#'
                    
                    if isInside is False: # Outside object

                        # Refracted Ray : Outside -> Inside
                        refractedRay = self.getRefractedRay(ray.direction, intersectionNormal, intersectionPointRefracted, n1, n2)
                        print 'REFRACTED RAY OUTSIDE'
                        print refractedRay.origin
                        print refractedRay.direction
                        if refractedRay != 0.0:
                            refractedColor = self.traceRay(refractedRay, iteration+1, refractionImportance, True, depth+1, 'refraction')
                            accPixelValue =  np.add(accPixelValue, refractedColor)
                            #accPixelValue =  np.add(accPixelValue, np.multiply(refractionImportance, refractedColor))

                    else: # Inside object

                        #Check Critical Angle
                        if np.arcsin(n2 / n1) > np.arccos(np.dot(-intersectionNormal, ray.direction)):

                            #Refracted Ray : Inside -> Outside
                            refractedRay = self.getRefractedRay(ray.direction, intersectionNormal, intersectionPointRefracted, n1, n2)
                            print 'REFRACTED RAY INSIDE'
                            print refractedRay.origin
                            print refractedRay.direction
                            if refractedRay != 0.0:
                                refractedColor = self.traceRay(refractedRay, iteration+1, refractionImportance, False, depth+1, 'refraction')
                                accPixelValue =  np.add(accPixelValue, refractedColor)
                                #accPixelValue =  np.add(accPixelValue, np.multiply(refractionImportance, refractedColor))

                        else:
                            reflectionImportance = importance
                
                reflectedRay = self.getSpecularRay(ray.direction, intersectionNormal, intersectionPointReflected)
                print 'REFLECTED RAY'
                print reflectedRay.origin
                print reflectedRay.direction
                print ' '
                reflectionColor = self.traceRay(reflectedRay, iteration+1, reflectionImportance, isInside, depth+1, 'reflection')

                accPixelValue =  np.add(accPixelValue, reflectionColor)
                #accPixelValue =  np.add(accPixelValue, np.multiply(reflectionImportance, reflectionColor))
                '''
            



            # Direct Light
            directLight = [0.0, 0.0, 0.0, 1.0]
            intersectionPoint = ray.origin + ray.direction * (tClose - 0.01)
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
            #indirectColor = np.multiply((1.0 - firstGeometry.Material.getDiffuse()), np.multiply(importance, accPixelValue))
            indirectColor = np.multiply((1.0 - firstGeometry.Material.getDiffuse()), accPixelValue)

            totalColor = np.add(indirectColor, directColor)

            #print depth
            #rint totalColor

            return totalColor


        def getSpecularRay(self, incomingDirection, intersectNormal, intersectPoint):
            #direction = incomingDirection
            #directionNorm = 1/LA.norm(direction)
            #direction = np.multiply(direction, directionNorm)
            newDir = np.subtract(incomingDirection, np.multiply(np.multiply(2.0, np.dot(incomingDirection, intersectNormal)), intersectNormal) )
            newDirNormed = newDir / LA.norm(newDir)
            newRay = Ray(newDir, intersectPoint + (0.0001 * newDirNormed))
            return newRay

        def getRefractedRay(self, rayDirection, intersectNormal, intersectPoint, n1, n2):
            a = n1 / n2
            b = np.dot((-1 * rayDirection), intersectNormal)
            newDirection = (a * rayDirection) + np.multiply(((a * b) - np.sqrt(1 - ((a * a) * (1 - (b * b))))), intersectNormal)
            newDirectionNormed = newDirection / LA.norm(newDirection)
            newRay = Ray(newDirection, intersectPoint + (0.00001 * newDirectionNormed))
            return newRay

        def getRefractedContribution(self, intersectionPoint, normal, geometryObject, ray, n1, n2, importance, isInside, depth):
            Irefraction = 1 - importance

            eta = n1 / n2
            c1 = np.dot(ray.direction, normal) # cos(theta1)
            cs2 = 1 - eta*eta * (1 - c1*c1)     # cos^2(theta2)
            #print cs2
            if cs2 < 0.0 or depth > 10:
                return 0.0

            #newdirection = eta * ray.direction + (eta*c1-np.sqrt(cs2)* normal)
            component = -(eta * c1) - (np.sqrt(1 - ((eta*eta) * (1 - (c1*c1)))))
            newdirection = eta * ray.direction + normal * component
            #materialColor = geometryObject.Material.getColor()
            #materialColor = [materialColor[0], materialColor[1], materialColor[2], 1.0]
            newRay = Ray(newdirection, [0.0, 0.0, 0.0]) # numpy copy
            newRay.origin = ray.origin + 0.01*ray.direction
            return newRay
            #return (self.traceRay(newRay, iteration+1, Irefraction, True))


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
                        ambient = [0.2, 0.2, 0.2] * geometryObjectColor
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



