#intransparent.py

import numpy as np

from material import *



class Light(Material):

	#constructor
	def __init__(self):
		super(Light, self).__init__()
		super(Light, self).setColor(1.0, 1.0, 0.8)
		#super(Light, self).setReflection()
		#super(Light, self).setRefraction()
		#super(Light, self).setDiffuse()
		#super(Light, self).setSpecular()
		#super(Light, self).setSpecularPower()
		#super(Light, self).setIOR()
		super(Light, self).setRadiance(4000)
		super(Light, self).setLight(True)
		super(Light, self).setWall(False)
		super(Light, self).setTransparency(False)