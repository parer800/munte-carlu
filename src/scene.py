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

		# Create all material object
		material_1 = Material()
		material_1.setColor(1.0, 0.0, 0.0)

		material_2 = Material()
		material_2.setColor(0.0, 0.0, 1.0)

		material_3 = Material()
		material_3.setColor(0.0, 1.0, 0.0)


		# Create all geometry objects.
		planeBack = Plane(material_1)
		planeBack.setPosition(0.0, 0.0, 0.0)
		planeBack.setNormal(0.0, 0.0, 1.0)
		planeBack.setWidth(100.0)
		planeBack.setHeight(100.0)

		planeLeft = Plane(material_2)
		planeLeft.setPosition(0.0, 0.0, 100.0)
		planeLeft.setNormal(1.0, 0.0, 0.0)
		planeLeft.setWidth(100.0)
		planeLeft.setHeight(100.0)
		
		planeRight = Plane(material_3)
		planeRight.setPosition(100.0, 0.0, 100.0)
		planeRight.setNormal(-1.0, 0.0, 0.0)
		planeRight.setWidth(100.0)
		planeRight.setHeight(100.0)
		

		# Append all geometry objects.
		self.sceneGeometry.append(planeBack)
		self.sceneGeometry.append(planeLeft)
		self.sceneGeometry.append(planeRight)

