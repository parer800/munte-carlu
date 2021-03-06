#transparent.py

import numpy as np

from material import *



class Transparent(Material):

	#constructor
	def __init__(self):
		super(Transparent, self).__init__()
		super(Transparent, self).setColor(0.0, 0.0, 1.0)
		super(Transparent, self).setReflection(0.3)
		super(Transparent, self).setRefraction(1.5)
		super(Transparent, self).setDiffuse(0.1)
		super(Transparent, self).setSpecular(0.95)
		super(Transparent, self).setSpecularPower(96.0)
		super(Transparent, self).setIOR(1.5)
		#super(Transparent, self).setRadiance()
		super(Transparent, self).setLight(False)
		super(Transparent, self).setWall(False)
		super(Transparent, self).setTransparency(True)