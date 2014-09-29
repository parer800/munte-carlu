#!/usr/bin/python
# coding: utf-8
#tracer.py, Class for the actual Ray Tracer

import numpy as np
import random as rand

from OpenGL.GL import *
from OpenGL.GLUT import *
from scene import *
from ray import *

class Tracer():

	# Constructor Tracer
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.Scene = Scene(np.array([50.0, 50.0, 189.0]), 45.0, (width / height))

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
		ray = Ray(rayDirection, rayOrigin)

		# Russian Roulette random variable
		rr = rand.random()

		# Pixel Color
		pixelColor = [0.0, 0.0, 0.0, 0.0]

		# Check first intersection
		tClose = 9999

		# Go through all geometry in the scene
		geometry = self.Scene.sceneGeometry
		for g in range(len(geometry)):
			matColor = geometry[g].Material.getColor()
			t = geometry[g].intersect(ray)
			if t > 0 and t < tClose:
				tClose = t
				pixelColor =  [matColor[0], matColor[1], matColor[2], 1.0]



		

		return pixelColor

		


		