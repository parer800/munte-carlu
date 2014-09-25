#!/usr/bin/python
# coding: utf-8
#render.py, Class for rendering

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from tracer import *

class Render():

	# Constructor Renderer
	def __init__(self, width, height):
		self.pixelData = None
		self.width = width
		self.height = height
		self.Tracer = Tracer(width, height)

	# Init Renderer
	def init(self):
		self.Tracer.init()

		pixelData = [0] * (self.width * self.height)
		for y in range(0, self.height):
			for x in range(0, self.width):
				pixelData[x + (y * self.height)] = self.createPixel(x, y)

		self.pixelData = pixelData

	# Render a single pixel
	def createPixel(self, x, y):
		return self.Tracer.castRay()

	# Draw Renderer
	def draw(self):
		glRasterPos2i(-1 , -1)
		glDrawPixels(self.width , self.height , GL_RGBA , GL_FLOAT , self.pixelData)