#!/usr/bin/python
# coding: utf-8
#scene.py, Class for managing the scene

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from sphere import *

class Scene():

	# Constructor Scene
	def __init__(self, imageWidth, imageHeight, cameraPos, fieldOfView, viewDirection = np.array([0.0, 0.0, -1.0])):
		self.imageWidth = imageWidth # Image plane width.
		self.imageHeight = imageHeight # Image plane height.
		self.cameraPos = cameraPos # Global camera position.
		self.fieldOfView = fieldOfView # Field of View for camera to view plane.
		self.viewDirection = viewDirection # View direction of camera.
		self.sceneGeometry = [] # Contains all geometry in the scene, Cornell Box.

	def setupScene(self):

		# Create all geometry objects.
		sphere = Sphere()

		# Append all geometry objects.
		self.sceneGeometry.append(sphere)
