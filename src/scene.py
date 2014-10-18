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
		materialDiffuseRed.setColor(1.0, 0.0, 0.0)

		materialDiffuseBlue = Material()
		materialDiffuseBlue.setColor(0.0, 0.0, 1.0)

		materialWhite = Material()
		materialWhite.setColor(1.0, 1.0, 1.0)

		materialGrey = Material()
		materialGrey.setColor(0.5, 0.5, 0.5)

		materialBlack = Material()
		materialBlack.setColor(0.0, 0.0, 0.0)

		materialGreen = Material()
		materialGreen.setColor(0.0, 1.0, 0.0)

		materialSphere1 = Material()
		materialSphere1.setColor(0.3, 1.0, 0.8)


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
		planeLeft.setPointSouthWest(0.0, 0.0, 100.0)
		planeLeft.setPointNorthWest(0.0, 100.0, 100.0)
		planeLeft.setPointNorthEast(0.0, 100.0, 0.0)
		planeLeft.setPointSouthEast(0.0, 0.0, 0.0)
		planeLeft.setNormal(1.0, 0.0, 0.0)
		
		# Wall Right
		planeRight = Plane(materialDiffuseBlue)
		planeRight.setPointSouthWest(150.0, 0.0, 0.0)
		planeRight.setPointNorthWest(150.0, 100.0, 0.0)
		planeRight.setPointNorthEast(150.0, 100.0, 100.0)
		planeRight.setPointSouthEast(150.0, 0.0, 100.0)
		planeRight.setNormal(-1.0, 0.0, 0.0)

		# Roof
		planeUp = Plane(materialBlack)
		planeUp.setPointSouthWest(0.0, 100.0, 100.0)
		planeUp.setPointNorthWest(150.0, 100.0, 100.0)
		planeUp.setPointNorthEast(150.0, 100.0, 0.0)
		planeUp.setPointSouthEast(0.0, 100.0, 0.0)
		planeUp.setNormal(0.0, -1.0, 0.0)
		
		# Floor
		planeDown = Plane(materialGreen)
		planeDown.setPointSouthWest(0.0, 0.0, 0.0)
		planeDown.setPointNorthWest(150.0, 0.0, 0.0)
		planeDown.setPointNorthEast(150.0, 0.0, 100.0)
		planeDown.setPointSouthEast(0.0, 0.0, 100.0)
		planeDown.setNormal(0.0, 1.0, 0.0)

		# Light Source
		areaLightSource = Plane(materialWhite)
		areaLightSource.setPointSouthWest(30.0, 99.0, 60.0)
		areaLightSource.setPointNorthWest(70.0, 99.0, 60.0)
		areaLightSource.setPointNorthEast(70.0, 99.0, 40.0)
		areaLightSource.setPointSouthEast(30.0, 99.0, 40.0)
		areaLightSource.setNormal(0.0, -1.0, 0.0)

		# Sphere 1
		sphere1 = Sphere(materialSphere1)
		sphere1.setRadius(20.0)
		sphere1.setCenterPoint(np.array([30.0, 25.0, 30.0]))
		

		# Append all geometry objects.
		self.sceneGeometry.append(planeBack)
		self.sceneGeometry.append(planeLeft)
		self.sceneGeometry.append(planeRight)
		self.sceneGeometry.append(planeUp)
		self.sceneGeometry.append(planeDown)
		self.sceneGeometry.append(areaLightSource)
		self.sceneGeometry.append(sphere1)
		

