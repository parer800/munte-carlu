#!/usr/bin/python
# coding: utf-8
#tracer.py, Class for the actual Ray Tracer

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from scene import *
from ray import *

class Tracer():

	# Constructor Tracer
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.Scene = Scene(np.array([50.0, 50.0, 200.0]), 45.0, (width / height))

	# Init Tracer
	def init(self):
		self.Scene.setupScene()


	def traceRay(self, pixelPosX, pixelPosY):

		# Calculate ray origin and direction
		rayDirection = np.array([0.0, 0.0, 0.0])
		rayOrigin = np.array([0.0, 0.0, 0.0])
		rayOrigin[0] = (pixelPosX / self.width) * (2 * self.Scene.cameraPos[0])
		rayOrigin[1] = (pixelPosY / self.height) * (2 * self.Scene.cameraPos[1])
		rayOrigin[2] = self.Scene.cameraPos[2] - ((1 / (np.tan(self.Scene.fovY/2))) * self.Scene.cameraPos[0])
		rayDirection = rayOrigin - self.Scene.cameraPos
		rayDirection = rayDirection / np.linalg.norm(rayDirection)

		# Spawn new ray
		singleRay = Ray(rayDirection, rayOrigin)

		# Return pixel colors
		R = np.random.random()
		G = np.random.random()
		B = np.random.random()
		A = np.random.random()
		return [R, G, B, A]