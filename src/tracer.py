#!/usr/bin/python
# coding: utf-8
#tracer.py, Class for the actual Ray Tracer
from OpenGL.GL.NV import half_float
from OpenGLContext.resources import lights_vert_txt
import copy
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

        def traceRay(self, ray, iteration, importance, isInside, depth=0):


            # IF number of iterations > Maxiterations OR importance < minimiimportance
            if iteration > 20:
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
                return [lightColor[0], lightColor[1], lightColor[2], 1.0]


            # IF reflective or refractive object
            # PUT SOME CODE HERE FOR THAT! RETURN accPixelValue
            reflection = firstGeometry.Material.getReflection()
            refraction = firstGeometry.Material.getRefraction()
            intersectionPoint = ray.origin + ray.direction * tClose

           # print tClose
            intersectionNormal = firstGeometry.getNormal(intersectionPoint)

            #new ray direction & origin point
            newRay = Ray(intersectionNormal, intersectionPoint)
            accPixelValue =  [0.0, 0.0, 0.0, 1.0]
            refractedColor = [0.0, 0.0, 0.0, 1.0]
            #Perfectly specular: use reflected ray

            if firstGeometry.Material.getLight() is False and firstGeometry.Material.getWall() is False:
                #Refractive and Reflective
               # print ray.direction
                refractedRay = copy.copy(ray)
               # print ray.direction
                #print specularRay.direction
                #Perfect reflection direction ()
                EPSILON = 0.01*ray.direction

                #print specularRay

                reflection = firstGeometry.Material.getReflection()
                reflectionImportance = reflection
                #TODO implement refraction
                if firstGeometry.Material.getTransparency() is True:
                    #Transparent
                  #  print "Transparent"
                    refraction = firstGeometry.Material.getRefraction()
                    refractionImportance = 1-reflectionImportance


                    normal = firstGeometry.getNormal(intersectionPoint)
                    if isInside is False:
                        #outside n1 = 1.0
                        n1 = 1.0
                        n2 = firstGeometry.Material.getIOR()
                        isInside = True # next recursion True
                    else:
                        #inside n1 = material's IOR
                        n1 = firstGeometry.Material.getIOR()
                        n2 = 1.0
                        normal = -normal
                        isInside = False # next recursion False
                    #refractedColor = self.getRefractedContribution(intersectionPoint, refractedRay.direction, firstGeometry, refractedRay, iteration, importance, isInside)
                    #print isInside
                    refractedRay = self.getRefractedContribution(intersectionPoint, normal, firstGeometry, ray, n1, n2, refractionImportance, isInside, depth)
                    #print refractedRay
                    if refractedRay != 0.0:
                        ray.origin = refractedRay.origin
                        ray.direction = refractedRay.direction
                        refractedColor = self.traceRay(ray, iteration+1, refractionImportance, isInside, depth+1)

                #print refractedColor


                # Not used yet, but wil affect the importnace



                #material color for the specular object
                materialColor = firstGeometry.Material.getColor()
                materialColor = [materialColor[0], materialColor[1], materialColor[2], 1.0]
               # print ray.direction

                ray.origin = newRay.origin - EPSILON
                ray.direction = self.getSpecularRay(ray.direction, intersectionNormal, intersectionPoint)
                accPixelValue =  (self.traceRay(ray, iteration+1, reflectionImportance, False, depth+1) + np.array(refractedColor))



            # ELSE IF diffuse lambertian BRDF
            # PUT SOME CODE HERE FOR THAT! RETURN accPixelValue
            # Monte-Carlo BRDF
            '''
            elif firstGeometry.Material.getWall() == True:
                rr = rand.random()
                if rr < 0.5: # STATIC VALUE KAN ÄNDRAS TILL ANNAT VÄRDE
                    intersectionPoint = ray.origin + ray.direction * tClose
                    newRay = calculateDiffuseRay(ray.direction, firstGeometry.getNormal(intersectionPoint))
                    #accPixelValue = traceRay(newRay, iteration+1, importance):
            '''



            # Calculate shadow ray            
            intersectionPoint = ray.origin + ray.direction * tClose
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                 if geometry[g].Material.getLight() == True:
                    lightPoint = geometry[g].getRandomPoint()
                    lightVec = lightPoint - intersectionPoint
                    
                    if self.calculateShadow(intersectionPoint, lightVec):
                        return [0.0, 0.0, 0.0, 1.0]


            directLight =  self.calculateDirectLight(intersectionPoint, firstGeometry, ray)
            # Return value

            #return (np.add(accPixelValue, directLight, refractedColor))
            return np.array(directLight) + np.multiply(accPixelValue, importance)
            #return (accPixelValue + objectColor + lambert * lambert * shade * phong * diffuse * lightColor)

        def getSpecularContribution(self, ray, object, iteration, importance):
                reflection = object.Material.getReflection()
                #Ireflection = importance*reflection
                materialColor = object.Material.getColor()
                materialColor = [materialColor[0], materialColor[1], materialColor[2], 1.0]
                #ray.origin = ray.origin + ray.direction * 10
                return (np.multiply(materialColor, 0.9) + np.multiply(self.traceRay(ray, iteration+1, 1.0, False),0.1))


        def getSpecularRay(self, ray, intersectNormal, intersectPoint):
            direction = ray.copy()
            directionNorm = 1/LA.norm(direction)
            direction = np.multiply(direction, directionNorm)
            newDir = np.subtract(direction, np.multiply(np.multiply(2.0, np.dot(direction, intersectNormal)), intersectNormal) )
            newDir = newDir / LA.norm(newDir)

            return newDir


        def getRefractedContribution(self, intersectionPoint, normal, geometryObject, ray, n1, n2, importance, isInside, depth):
            Irefraction = 1 - importance


            eta = n1 / n2
            c1 = np.dot(ray.direction, normal) # cos(theta1)
            cs2 = 1 - eta*eta * (1 - c1*c1)     # cos^2(theta2)
            #print cs2
            if cs2 < 0.0 or depth > 10:                       # total internal reflection
                return 0.0

            #newdirection = eta * ray.direction + (eta*c1-np.sqrt(cs2)* normal)
            component = -eta * c1 - (np.sqrt(1 - ((eta*eta) * (1 - (c1*c1)))))
            newdirection = eta * ray.direction + normal * component
            #materialColor = geometryObject.Material.getColor()
            #materialColor = [materialColor[0], materialColor[1], materialColor[2], 1.0]
            newRay = Ray(newdirection, [0.0, 0.0, 0.0]) # numpy copy
            newRay.origin = ray.origin + 0.001*ray.direction
            return newRay
            #return (self.traceRay(newRay, iteration+1, Irefraction, True))

            '''if isInside is False:
                #outside n1 = 1.0
                n1 = 1.0
                n2 = geometryObject.Material.getIOR()
            else:
                #inside n1 = material's IOR
                n1 = geometryObject.Material.getIOR()
                n2 = 1.0
                normal = -normal'''



            '''NdotI = np.dot(normal, ray.direction)
            #print NdotI
          # print (1-((n1/n2)**2) * ((1 - NdotI)**2))
            component = -(n1/n2) * NdotI - (np.sqrt(1 - (((n1/n2)**2) * (1 - (NdotI)**2))))
            direction = (n1/n2) * reflectedRay + normal * component
            #print "n1 %f n2 %f" % (n1, n2)

            #Color of
            materialColor = geometryObject.Material.getColor()
            materialColor = [materialColor[0], materialColor[1], materialColor[2], 1.0]
            newRay = Ray(ray.direction.copy(), [0.0, 0.0, 0.0]) # numpy copy
            newRay.origin = ray.origin.copy() + 0.001*ray.direction.copy()
            return (np.multiply(materialColor, importance) + np.multiply(self.traceRay(newRay, iteration+1, Irefraction, True),0.1))'''


        def calculateDiffuseRay(rayDirection, pointNormal):
            # FORTSÄTT HÄR!
            return 0.0

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
                    color = (geometryObjectColor * diffuse + specular) * lightColor

                    return [color[0], color[1], color[2], 1.0]
                    #return self.blinnPhong(intersectionPoint, geometryObject, ray)

        def blinnPhong(self, intersectionPoint, geometryObject, ray):
            geometry = self.Scene.sceneGeometry
            for g in range(len(geometry)):
                if (geometry[g].Material.getLight()):
                    lightSource = geometry[g]
                    lightPoint = lightSource.getRandomPoint()
                    lightVec =   lightPoint - intersectionPoint
                    blinnDir = lightVec - ray.direction
                    check = (np.dot(blinnDir, blinnDir))**0.5
                    if check != 0.0:
                        lightVec = lightVec / LA.norm(lightVec)
                        halfVector  = lightVec + ray.direction
                        halfVector = halfVector/LA.norm(halfVector)
                        normal = geometryObject.getNormal(intersectionPoint)
                        specTmp = np.max(np.dot(normal, halfVector), 0.0)
                        specularIntensity = specTmp**(geometryObject.Material.getSpecularPower())

                        NdotL = np.dot(normal, lightVec)
                        intensity = np.clip(NdotL, 0, 1)


                        materialColor = geometryObject.Material.getColor()
                        materialColor = [materialColor[0], materialColor[1], materialColor[2]]
                        color = np.multiply(materialColor, intensity)
                        out = [color[0], color[1], color[2], 1.0]
                        #print out
                        return out


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



