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
		materialDiffuseRed = Diffuse()
		materialDiffuseRed.setColor(0.3, 0.3, 0.3)

		materialDiffuseBlue = Material()
		materialDiffuseBlue.setColor(0.4, 0.4, 0.4)

		materialWhite = Material()
		materialWhite.setColor(1.0, 1.0, 1.0)

		materialGrey = Material()
		materialGrey.setColor(0.6, 0.6, 0.6)

		materialBlack = Material()
		materialBlack.setColor(0.2, 0.2, 0.2)

		materialGreen = Material()
		materialGreen.setColor(0.7, 0.7, 0.7)

		materialSphere1 = Material()
		materialSphere1.setColor(0.3, 1.0, 0.3)

		materialSphere2 = Material()
		materialSphere2.setColor(0.1, 0.5, 0.8)

		materialBox1 = Material()
		materialBox1.setColor(0.8, 0.1, 0.3)

		materialBox2 = Material()
		materialBox2.setColor(0.7, 0.1, 0.2)

		materialBox3 = Material()
		materialBox3.setColor(0.6, 0.0, 0.3)


		# CREATE ALL GEOMETRY

		# Wall Back
		planeBack = Plane(materialGrey)
		planeBack.setPointSouthWest(0.0, 0.0, 0.0)
		planeBack.setPointNorthWest(0.0, 100.0, 0.0)
		planeBack.setPointNorthEast(150.0, 100.0, 0.0)
		planeBack.setPointSouthEast(150.0, 0.0, 0.0)
		planeBack.setNormal(0.0, 0.0, 1.0)

		# Wall Left
		planeLeft = Plane(materialDiffuseRed)
		planeLeft.setPointSouthWest(0.0, 0.0, 120.0)
		planeLeft.setPointNorthWest(0.0, 100.0, 120.0)
		planeLeft.setPointNorthEast(0.0, 100.0, 0.0)
		planeLeft.setPointSouthEast(0.0, 0.0, 0.0)
		planeLeft.setNormal(1.0, 0.0, 0.0)
		
		# Wall Right
		planeRight = Plane(materialDiffuseBlue)
		planeRight.setPointSouthWest(150.0, 0.0, 0.0)
		planeRight.setPointNorthWest(150.0, 100.0, 0.0)
		planeRight.setPointNorthEast(150.0, 100.0, 120.0)
		planeRight.setPointSouthEast(150.0, 0.0, 120.0)
		planeRight.setNormal(-1.0, 0.0, 0.0)

		# Roof
		planeUp = Plane(materialBlack)
		planeUp.setPointSouthWest(0.0, 100.0, 120.0)
		planeUp.setPointNorthWest(150.0, 100.0, 120.0)
		planeUp.setPointNorthEast(150.0, 100.0, 0.0)
		planeUp.setPointSouthEast(0.0, 100.0, 0.0)
		planeUp.setNormal(0.0, -1.0, 0.0)
		
		# Floor
		planeDown = Plane(materialGreen)
		planeDown.setPointSouthWest(0.0, 0.0, 0.0)
		planeDown.setPointNorthWest(150.0, 0.0, 0.0)
		planeDown.setPointNorthEast(150.0, 0.0, 120.0)
		planeDown.setPointSouthEast(0.0, 0.0, 120.0)
		planeDown.setNormal(0.0, 1.0, 0.0)

		# Light Source
		areaLightSource = Plane(materialWhite)
		areaLightSource.setPointSouthWest(25.0, 99.0, 80.0)
		areaLightSource.setPointNorthWest(65.0, 99.0, 80.0)
		areaLightSource.setPointNorthEast(65.0, 99.0, 60.0)
		areaLightSource.setPointSouthEast(25.0, 99.0, 60.0)
		areaLightSource.setNormal(0.0, -1.0, 0.0)

		# Sphere 1
		sphere1 = Sphere(materialSphere1)
		sphere1.setRadius(15.0)
		sphere1.setCenterPoint(np.array([100.0, 20.0, 80.0]))

		# Sphere 2
		sphere2 = Sphere(materialSphere2)
		sphere2.setRadius(20.0)
		sphere2.setCenterPoint(np.array([120.0, 40.0, 30.0]))

		# Box Face Up
		boxFaceUp = Plane(materialBox1)
		boxFaceUp.setPointSouthWest(5.0, 30.0, 50.0)
		boxFaceUp.setPointNorthWest(35.0, 30.0, 20.0)
		boxFaceUp.setPointNorthEast(65.0, 30.0, 50.0)
		boxFaceUp.setPointSouthEast(35.0, 30.0, 80.0)
		boxFaceUp.setNormal(0.0, 1.0, 0.0)

		# Box Face Down
		boxFaceDown = Plane(materialBox1)
		boxFaceDown.setPointNorthWest(5.0, 0.1, 50.0)
		boxFaceDown.setPointSouthWest(35.0, 0.1, 20.0)
		boxFaceDown.setPointSouthEast(65.0, 0.1, 50.0)
		boxFaceDown.setPointNorthEast(35.0, 0.1, 80.0)
		boxFaceDown.setNormal(0.0, -1.0, 0.0)
		
		# Box Face Right
		boxFaceRight = Plane(materialBox1)
		boxFaceRight.setPointSouthWest(65.0, 0.1, 50.0)
		boxFaceRight.setPointNorthWest(65.0, 30.0, 50.0)
		boxFaceRight.setPointNorthEast(35.0, 30.0, 20.0)
		boxFaceRight.setPointSouthEast(35.0, 0.1, 20.0)
		boxFaceRight.setNormal((1/np.sqrt(2)), 0.0, -(1/np.sqrt(2)))

		# Box Face Left
		boxFaceLeft = Plane(materialBox2)
		boxFaceLeft.setPointSouthWest(5.0, 0.1, 50.0)
		boxFaceLeft.setPointNorthWest(5.0, 30.0, 50.0)
		boxFaceLeft.setPointNorthEast(35.0, 30.0, 80.0)
		boxFaceLeft.setPointSouthEast(35.0, 0.1, 80.0)
		boxFaceLeft.setNormal(-(1/np.sqrt(2)), 0.0, (1/np.sqrt(2)))
		
		# Box Face Back
		boxFaceBack = Plane(materialBox1)
		boxFaceBack.setPointSouthWest(35.0, 0.1, 20.0)
		boxFaceBack.setPointNorthWest(35.0, 30.0, 20.0)
		boxFaceBack.setPointNorthEast(5.0, 30.0, 50.0)
		boxFaceBack.setPointSouthEast(5.0, 0.1, 50.0)
		boxFaceBack.setNormal(-(1/np.sqrt(2)), 0.0, -(1/np.sqrt(2)))

		# Box Face Front
		boxFaceFront = Plane(materialBox3)
		boxFaceFront.setPointSouthWest(35.0, 0.1, 80.0)
		boxFaceFront.setPointNorthWest(35.0, 30.0, 80.0)
		boxFaceFront.setPointNorthEast(65.0, 30.0, 50.0)
		boxFaceFront.setPointSouthEast(65.0, 0.1, 50.0)
		boxFaceFront.setNormal((1/np.sqrt(2)), 0.0, (1/np.sqrt(2)))
		


		# Append all geometry objects.
		self.sceneGeometry.append(planeBack)
		self.sceneGeometry.append(planeLeft)
		self.sceneGeometry.append(planeRight)
		self.sceneGeometry.append(planeUp)
		self.sceneGeometry.append(planeDown)
		self.sceneGeometry.append(areaLightSource)
		self.sceneGeometry.append(sphere1)
		self.sceneGeometry.append(sphere2)
		self.sceneGeometry.append(boxFaceUp)
		self.sceneGeometry.append(boxFaceDown)
		self.sceneGeometry.append(boxFaceRight)
		self.sceneGeometry.append(boxFaceLeft)
		self.sceneGeometry.append(boxFaceBack)
		self.sceneGeometry.append(boxFaceFront)
		

