#intransparent.py

import numpy as np

from material import *



class Opaque(Material):

	#constructor
	def __init__(self):
		super(Opaque, self).__init__()
		super(Opaque, self).setColor(0.0, 1.0, 0.0)
		super(Opaque, self).setReflection(0.5)
		super(Opaque, self).setRefraction(0.0)
		super(Opaque, self).setDiffuse(0.5)
		super(Opaque, self).setSpecular(0.5)
		super(Opaque, self).setSpecularPower(50.0)
		#super(Opaque, self).setIOR()
		#super(Opaque, self).setRadiance()
		super(Opaque, self).setLight(False)
		super(Opaque, self).setWall(False)
		super(Opaque, self).setTransparency(False)
