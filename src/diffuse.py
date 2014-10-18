#Diffuse.py

import numpy as np

from material import *



class Diffuse(Material):
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
		super(Diffuse, self).__init__()
		super(Diffuse, self).setColor(1.0, 0.0, 0.0)
		#super(Diffuse, self).setSpecularColor(np.array([1.0, 0.0, 0.0]))
		#super(Diffuse, self).setReflection()
		#super(Diffuse, self).setRefraction()
		#super(Diffuse, self).setDiffuse()
		#super(Diffuse, self).setIOR()