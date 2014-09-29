#!/usr/bin/python
# coding: utf-8
#scene.py, Class for managing the scene

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from sphere import *
from plane import *
from material import *

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

		# CREATE ALL MATERIAL
		materialRed = Material()
		materialRed.setColor(1.0, 0.0, 0.0)

		materialBlue = Material()
		materialBlue.setColor(0.0, 0.0, 1.0)

		materialWhite = Material()
		materialWhite.setColor(1.0, 1.0, 1.0)

		materialGrey = Material()
		materialGrey.setColor(0.5, 0.5, 0.5)

		materialBlack = Material()
		materialBlack.setColor(0.0, 0.0, 0.0)

		materialGreen = Material()
		materialGreen.setColor(0.0, 1.0, 0.0)


		# CREATE ALL GEOMETRY

		# Wall Back
		planeBack = Plane(materialGrey)
		planeBack.setPointSouthWest(0.0, 0.0, 0.0)
		planeBack.setPointNorthWest(0.0, 100.0, 0.0)
		planeBack.setPointNorthEast(100.0, 100.0, 0.0)
		planeBack.setPointSouthEast(100.0, 0.0, 0.0)
		planeBack.setNormal(0.0, 0.0, 1.0)

		# Wall Left
		planeLeft = Plane(materialRed)
		planeLeft.setPointSouthWest(0.0, 0.0, 100.0)
		planeLeft.setPointNorthWest(0.0, 100.0, 100.0)
		planeLeft.setPointNorthEast(0.0, 100.0, 0.0)
		planeLeft.setPointSouthEast(0.0, 0.0, 0.0)
		planeLeft.setNormal(1.0, 0.0, 0.0)
		
		# Wall Right
		planeRight = Plane(materialBlue)
		planeRight.setPointSouthWest(100.0, 0.0, 0.0)
		planeRight.setPointNorthWest(100.0, 100.0, 0.0)
		planeRight.setPointNorthEast(100.0, 100.0, 100.0)
		planeRight.setPointSouthEast(100.0, 0.0, 100.0)
		planeRight.setNormal(-1.0, 0.0, 0.0)

		# Roof
		planeUp = Plane(materialBlack)
		planeUp.setPointSouthWest(0.0, 100.0, 100.0)
		planeUp.setPointNorthWest(100.0, 100.0, 100.0)
		planeUp.setPointNorthEast(100.0, 100.0, 0.0)
		planeUp.setPointSouthEast(0.0, 100.0, 0.0)
		planeUp.setNormal(0.0, -1.0, 0.0)
		
		# Floor
		planeDown = Plane(materialGreen)
		planeDown.setPointSouthWest(0.0, 0.0, 0.0)
		planeDown.setPointNorthWest(100.0, 0.0, 0.0)
		planeDown.setPointNorthEast(100.0, 0.0, 100.0)
		planeDown.setPointSouthEast(0.0, 0.0, 100.0)
		planeDown.setNormal(0.0, 1.0, 0.0)

		areaLightSource = Plane(materialWhite)
		areaLightSource.setPointSouthWest(30.0, 99.0, 60.0)
		areaLightSource.setPointNorthWest(70.0, 99.0, 60.0)
		areaLightSource.setPointNorthEast(70.0, 99.0, 40.0)
		areaLightSource.setPointSouthEast(30.0, 99.0, 40.0)
		areaLightSource.setNormal(0.0, -1.0, 0.0)
		

		# Append all geometry objects.
		self.sceneGeometry.append(planeBack)
		self.sceneGeometry.append(planeLeft)
		self.sceneGeometry.append(planeRight)
		self.sceneGeometry.append(planeUp)
		self.sceneGeometry.append(planeDown)
		self.sceneGeometry.append(areaLightSource)
		

