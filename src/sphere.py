#Sphere.py

import numpy as np

from geometry import Geometry

class Sphere(Geometry):
	"""A class for sphere objects
	radius: Sphere's radius
	"""

	#constructor
	def __init__(self, radius=1):
		print "Inside Sphere init"
		super(Geometry, self).__init__()
		self.radius = radius


	#================================================================
	#========================== SETTERS =============================
	#================================================================
	
	#Set radius
	def setRadius(self, radius):
		self.radius = radius

	#================================================================
	#========================== GETTERS =============================
	#================================================================

	#Get radius
	def getRadius(self):
		return self.radius