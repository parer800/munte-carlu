#!/usr/bin/python
# coding: utf-8
#tracer.py, Class for the actual Ray Tracer

import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from scene import *

class Tracer():

	# Constructor Tracer
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.Scene = Scene(width, height, np.array([50.0, 50.0, 150.0]), 45.0)

	# Init Tracer
	def init(self):
		self.Scene.setupScene()


	def castRay(self):
		R = np.random.random()
		G = np.random.random()
		B = np.random.random()
		A = np.random.random()
		return [R, G, B, A]