#!/usr/bin/python
# coding: utf-8
#render.py, Class for rendering

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *


class Render():

	# Constructor Renderer
	def __init__(self, width, height):
		self.pixelData = None
		self.width = width
		self.height = height

	# Init Renderer
	def init(self):
		pixelData = [0] * (self.width * self.height)
		for y in range(0, self.height):
			for x in range(0, self.width):
				R = np.random.random()
				G = np.random.random()
				B = np.random.random()
				A = np.random.random()
				pixelData[x + (y * self.height)] = [R, G, B, A]
		self.pixelData = pixelData

	# Draw Renderer
	def draw(self):
		glRasterPos2i(-1 , -1)
		glDrawPixels(self.width , self.height , GL_RGBA , GL_FLOAT , self.pixelData)