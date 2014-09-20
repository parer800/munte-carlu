#geometry.py, base class for all geometry

import numpy as np

from material import Material

class Geometry(Material):
	"""A base class for geometry"""

	#constructor
	def __init__(self):
		print "Inside Geometry init"
		super(Material, self).__init__()



