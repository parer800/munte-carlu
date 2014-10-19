#Material.py

import numpy as np



class Material(object):

	#constructor
	def __init__(self):
		self.color = np.array([.0,.0,.0])

	#================================================================
	#========================== SETTERS =============================
	#================================================================

	#Set color with rgb
	def setColor(self, r, g, b):
		self.color = np.array([r, g, b])

	#Set Reflection
	def setReflection(self, reflection):
		self.reflection = reflection

	# Set refraction
	def setRefraction(self, refraction):
		self.refraction = refraction

	# Set diffuse
	def setDiffuse(self, diffuse):
		self.diffuse = diffuse

	#Sets how much a ray traveling through the material will be refracted
	def setIOR(self, IOR):
		self.IOR = IOR

	#Sets radiance for light sources
	def setRadiance(self, radiance):
		self.radiance = radiance

	#Sets radiance for light sources
	def setLight(self, light):
		self.light = light


	#================================================================
	#========================== GETTERS =============================
	#================================================================

	#Get color
	def getColor(self):
		return self.color

	#Get reflection
	def getReflection(self):
		return self.reflection

	#get Refraction
	def getRefraction(self):
		return self.refraction

	#Get diffuse
	def getDiffuse(self):
		return self.diffuse

	#Get IOR
	def getIOR(self):
		return self.IOR

	#Get radiance
	def getRadiance(self):
		return self.radiance

	#Get radiance
	def getLight(self):
		return self.light



