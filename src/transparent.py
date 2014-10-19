#transparent.py

import numpy as np

from material import *



class Transparent(Material):

	#constructor
	def __init__(self):
		super(Transparent, self).__init__()
		super(Transparent, self).setColor(0.0, 0.0, 1.0)
		super(Transparent, self).setReflection(0.5)
		super(Transparent, self).setRefraction(1.5)
		super(Transparent, self).setDiffuse(0.0)
		#super(Transparent, self).setIOR()
		#super(Transparent, self).setRadiance()
		super(Transparent, self).setLight(False)