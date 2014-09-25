#!/usr/bin/python
# coding: utf-8
#scene.py, Class for managing the scene

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from sphere import *

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

		# Create all geometry objects.
		sphere = Sphere()

		# Append all geometry objects.
		self.sceneGeometry.append(sphere)

