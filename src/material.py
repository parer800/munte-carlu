#Material.py

import numpy as np



class Material(object):
	"""A class for material attributes
	color: 			material's color
	specularColor: 	material's specular color
	reflection:		material's reflection constant
	refraction:		material's refraction
	diffuse:		material's diffuse
	IOR: 			material's index of refraction
	"""

	#constructor
	def __init__(self):
		self.color = np.array([.0,.0,.0])

	#================================================================
	#========================== SETTERS =============================
	#================================================================

	#Set color with an array
	def setColor(self, color=np.array([.0,.0,.0])):
		self.color = color

	#Set color with rgb
	def setColor(self, r, g, b):
		self.color = np.array([r, g, b])

	#Set Specular color
	def setSpecularColor(self, specularColor = np.array([.0,.0,.0])):
		self.specularColor = specularColor

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


	#================================================================
	#========================== GETTERS =============================
	#================================================================

	#Get color
	def getColor(self):
		return self.color

	#Get specular color
	def getSpecularColor(self):
		return self.specularColor

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



