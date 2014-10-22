#Ray.py
import numpy as np
from numpy import linalg as LA


class Ray:
    def __init__(self, direction, origin):
        self.direction = np.array(direction)/LA.norm(direction)
        self.origin = np.array(origin)
