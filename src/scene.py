#!/usr/bin/python
# coding: utf-8
#scene.py, Class for managing the scene

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from sphere import *
from plane import *
from material import *
from diffuse import *
from transparent import *
from opaque import *
from light import *

class Scene():

    # Constructor Scene
    def __init__(self,  cameraPos, fovY, aspect, viewDirection = np.array([0.0, 0.0, -1.0])):
        self.cameraPos = cameraPos # Global camera position.
        self.fovY = fovY # Field of View for the Y-component.
        self.aspect = aspect # Aspect of x / y
        self.viewDirection = viewDirection # View direction of camera.
        self.sceneGeometry = [] # Contains all geometry in the scene, Cornell Box.

        # Setup scene geometry.
    def setupScene(self):

        '''

            1 Transparent obj
            1 Intransparent obj

            Objects (At least 3): Spheres, Cubes, Walls
            Light Sources: 2

            Transparet in Monte Carlo: Perfect reflection, refraction
            Intransparent in Monte Carlo: Monte Carlo Scheme, BRDF: Phong Reflection

            Starting importance for each pixel: 1/N, N = ray count
            Each Ray: Starting point, direction, importance, colour, information about children rays, outside/inside objects


        '''

        # CREATE ALL MATERIAL
        materialRoof = Diffuse()
        materialRoof.setColor(0.8, 0.8, 0.8)

        materialFloor = Diffuse()
        materialFloor.setColor(0.8, 0.8, 0.8)

        materialWallBack = Diffuse()
        materialWallBack.setColor(0.8, 0.8, 0.8)

        materialWallLeft = Diffuse()
        materialWallLeft.setColor(0.6, 0.0, 0.0)

        materialWallRight = Diffuse()
        materialWallRight.setColor(0.0, 0.6, 0.0)

        materialBox = Opaque()
        materialBox.setColor(0.5, 0.5, 0.5)

        materialGlassSphere = Transparent()
        materialGlassSphere.setColor(0.2, 0.2, 0.8)
        materialGlassSphere.setIOR(1.5)

        materialPlasticSphere = Opaque()
        materialPlasticSphere.setColor(0.8, 0.2, 0.2)

        materialLight = Light()


        # CREATE ALL GEOMETRY

        # Wall Back
        planeBack = Plane(materialWallBack)
        planeBack.setName("WallBack")
        planeBack.setPointSouthWest(0.0, 0.0, 0.0)
        planeBack.setPointNorthWest(0.0, 100.0, 0.0)
        planeBack.setPointNorthEast(150.0, 100.0, 0.0)
        planeBack.setPointSouthEast(150.0, 0.0, 0.0)
        planeBack.setNormal(0.0, 0.0, 1.0)

        # Wall Left
        planeLeft = Plane(materialWallLeft)
        planeLeft.setName("WallLeft")
        planeLeft.setPointSouthWest(0.0, 0.0, 120.0)
        planeLeft.setPointNorthWest(0.0, 100.0, 120.0)
        planeLeft.setPointNorthEast(0.0, 100.0, 0.0)
        planeLeft.setPointSouthEast(0.0, 0.0, 0.0)
        planeLeft.setNormal(1.0, 0.0, 0.0)

        # Wall Right
        planeRight = Plane(materialWallRight)
        planeRight.setName("WallRight")
        planeRight.setPointSouthWest(150.0, 0.0, 0.0)
        planeRight.setPointNorthWest(150.0, 100.0, 0.0)
        planeRight.setPointNorthEast(150.0, 100.0, 120.0)
        planeRight.setPointSouthEast(150.0, 0.0, 120.0)
        planeRight.setNormal(-1.0, 0.0, 0.0)

        # Roof
        planeUp = Plane(materialRoof)
        planeUp.setName("Roof")
        planeUp.setPointSouthWest(0.0, 100.0, 120.0)
        planeUp.setPointNorthWest(150.0, 100.0, 120.0)
        planeUp.setPointNorthEast(150.0, 100.0, 0.0)
        planeUp.setPointSouthEast(0.0, 100.0, 0.0)
        planeUp.setNormal(0.0, -1.0, 0.0)

        # Floor
        planeDown = Plane(materialFloor)
        planeDown.setName("Floor")
        planeDown.setPointSouthWest(0.0, 0.0, 0.0)
        planeDown.setPointNorthWest(150.0, 0.0, 0.0)
        planeDown.setPointNorthEast(150.0, 0.0, 120.0)
        planeDown.setPointSouthEast(0.0, 0.0, 120.0)
        planeDown.setNormal(0.0, 1.0, 0.0)

        # Light Source
        areaLightSource = Plane(materialLight)
        areaLightSource.setName("Light")
        areaLightSource.setPointSouthWest(25.0, 99.0, 80.0)
        areaLightSource.setPointNorthWest(65.0, 99.0, 80.0)
        areaLightSource.setPointNorthEast(65.0, 99.0, 60.0)
        areaLightSource.setPointSouthEast(25.0, 99.0, 60.0)
        areaLightSource.setNormal(0.0, -1.0, 0.0)

        # Sphere Front Transparent
        sphereTest = Sphere(materialPlasticSphere)
        sphereTest.setName("TestSphere")
        sphereTest.setRadius(15.0)
        sphereTest.setCenterPoint(np.array([50.0, 40.0, 30.0]))

        # Sphere Front Transparent
        sphere1 = Sphere(materialGlassSphere)
        sphere1.setName("GlassSphere")
        sphere1.setRadius(15.0)
        sphere1.setCenterPoint(np.array([100.0, 20.0, 80.0]))

        # Sphere Back Opaque
        sphere2 = Sphere(materialPlasticSphere)
        sphere2.setName("PlasticSphere")
        sphere2.setRadius(20.0)
        sphere2.setCenterPoint(np.array([120.0, 40.0, 30.0]))

        # Box Face Up
        boxFaceUp = Plane(materialBox)
        boxFaceUp.setName("BoxUp")
        boxFaceUp.setPointSouthWest(5.0, 40.0, 50.0)
        boxFaceUp.setPointNorthWest(35.0, 40.0, 20.0)
        boxFaceUp.setPointNorthEast(65.0, 40.0, 50.0)
        boxFaceUp.setPointSouthEast(35.0, 40.0, 80.0)
        boxFaceUp.setNormal(0.0, 1.0, 0.0)

        # Box Face Down
        boxFaceDown = Plane(materialBox)
        boxFaceDown.setName("BoxDown")
        boxFaceDown.setPointNorthWest(5.0, 0.1, 50.0)
        boxFaceDown.setPointSouthWest(35.0, 0.1, 20.0)
        boxFaceDown.setPointSouthEast(65.0, 0.1, 50.0)
        boxFaceDown.setPointNorthEast(35.0, 0.1, 80.0)
        boxFaceDown.setNormal(0.0, -1.0, 0.0)

        # Box Face Right
        boxFaceRight = Plane(materialBox)
        boxFaceRight.setName("BoxRight")
        boxFaceRight.setPointSouthWest(65.0, 0.1, 50.0)
        boxFaceRight.setPointNorthWest(65.0, 40.0, 50.0)
        boxFaceRight.setPointNorthEast(35.0, 40.0, 20.0)
        boxFaceRight.setPointSouthEast(35.0, 0.1, 20.0)
        boxFaceRight.setNormal((1/np.sqrt(2)), 0.0, -(1/np.sqrt(2)))

        # Box Face Left
        boxFaceLeft = Plane(materialBox)
        boxFaceLeft.setName("BoxLeft")
        boxFaceLeft.setPointSouthWest(5.0, 0.1, 50.0)
        boxFaceLeft.setPointNorthWest(5.0, 40.0, 50.0)
        boxFaceLeft.setPointNorthEast(35.0, 40.0, 80.0)
        boxFaceLeft.setPointSouthEast(35.0, 0.1, 80.0)
        boxFaceLeft.setNormal(-(1/np.sqrt(2)), 0.0, (1/np.sqrt(2)))

        # Box Face Back
        boxFaceBack = Plane(materialBox)
        boxFaceBack.setName("BoxBack")
        boxFaceBack.setPointSouthWest(35.0, 0.1, 20.0)
        boxFaceBack.setPointNorthWest(35.0, 40.0, 20.0)
        boxFaceBack.setPointNorthEast(5.0, 40.0, 50.0)
        boxFaceBack.setPointSouthEast(5.0, 0.1, 50.0)
        boxFaceBack.setNormal(-(1/np.sqrt(2)), 0.0, -(1/np.sqrt(2)))

        # Box Face Front
        boxFaceFront = Plane(materialBox)
        boxFaceFront.setName("BoxFront")
        boxFaceFront.setPointSouthWest(35.0, 0.1, 80.0)
        boxFaceFront.setPointNorthWest(35.0, 40.0, 80.0)
        boxFaceFront.setPointNorthEast(65.0, 40.0, 50.0)
        boxFaceFront.setPointSouthEast(65.0, 0.1, 50.0)
        boxFaceFront.setNormal((1/np.sqrt(2)), 0.0, (1/np.sqrt(2)))


        # Append all geometry objects.
        self.sceneGeometry.append(planeBack)
        self.sceneGeometry.append(planeLeft)
        self.sceneGeometry.append(planeRight)
        self.sceneGeometry.append(planeUp)
        self.sceneGeometry.append(planeDown)
        self.sceneGeometry.append(areaLightSource)
        self.sceneGeometry.append(sphereTest)

        self.sceneGeometry.append(sphere1)
'''
        self.sceneGeometry.append(sphere2)
        self.sceneGeometry.append(boxFaceUp)
        self.sceneGeometry.append(boxFaceDown)
        self.sceneGeometry.append(boxFaceRight)
        self.sceneGeometry.append(boxFaceLeft)
        self.sceneGeometry.append(boxFaceBack)
        self.sceneGeometry.append(boxFaceFront)
        '''

		

