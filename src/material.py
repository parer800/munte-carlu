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

	# Set specular
	def setSpecular(self, specular):
		self.specular = specular

	# Set specular power
	def setSpecularPower(self, specularPower):
		self.specularPower = specularPower

	#Sets how much a ray traveling through the material will be refracted
	def setIOR(self, IOR):
		self.IOR = IOR

	#Sets radiance for light sources
	def setRadiance(self, radiance):
		self.radiance = radiance

	#Sets is light
	def setLight(self, light):
		self.light = light

	#Sets is wall
	def setWall(self, wall):
		self.wall = wall

	#Sets is transparency
	def setTransparency(self, transparency):
		self.transparency = transparency


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

	# Get specular
	def getSpecular(self):
		return self.specular

	# Get specular power
	def getSpecularPower(self):
		return self.specularPower

	#Get IOR
	def getIOR(self):
		return self.IOR

	#Get radiance
	def getRadiance(self):
		return self.radiance

	#Get is light
	def getLight(self):
		return self.light

	#Get is wall
	def getWall(self):
		return self.wall

	#Get is transparency
	def getTransparency(self):
		return self.transparency



