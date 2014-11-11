#diffuse.py

import numpy as np

from material import *



class Diffuse(Material):

	#constructor
	def __init__(self):
		super(Diffuse, self).__init__()
		super(Diffuse, self).setColor(1.0, 0.0, 0.0)
		super(Diffuse, self).setReflection(0.9)#0.5
		super(Diffuse, self).setRefraction(0.0)
		super(Diffuse, self).setDiffuse(0.5) #0.7
		super(Diffuse, self).setSpecular(0.0225)
		super(Diffuse, self).setSpecularPower(12.8)
		#super(Diffuse, self).setIOR()
		#super(Diffuse, self).setRadiance()
		super(Diffuse, self).setLight(False)
		super(Diffuse, self).setWall(True)
		super(Diffuse, self).setTransparency(False)