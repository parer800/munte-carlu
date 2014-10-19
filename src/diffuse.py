#diffuse.py

import numpy as np

from material import *



class Diffuse(Material):

	#constructor
	def __init__(self):
		super(Diffuse, self).__init__()
		super(Diffuse, self).setColor(1.0, 0.0, 0.0)
		super(Diffuse, self).setReflection(0.0)
		super(Diffuse, self).setRefraction(0.0)
		super(Diffuse, self).setDiffuse(1.0)
		#super(Diffuse, self).setIOR()
		#super(Diffuse, self).setRadiance()
		super(Diffuse, self).setLight(False)
		super(Diffuse, self).setWall(True)
		super(Diffuse, self).setTransparency(False)