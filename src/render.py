#!/usr/bin/python
# coding: utf-8
#render.py, Class for rendering

import numpy as np
import time
import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from tracer import *

class Render():

    # Constructor Renderer
    def __init__(self, width, height):
        self.pixelData = None
        self.width = width
        self.height = height
        self.Tracer = Tracer(width, height)

    # Init Renderer
    def init(self):
        self.Tracer.init() # Init Tracer
        pixelData = [0] * (self.width * self.height)
        height = self.height
        width = self.width
        createPixel = self.createPixel

        sys.stdout.write("[%s]" % (" " * 100))
        sys.stdout.flush()
        sys.stdout.write("\b" * (100 + 1))

        for y in range(0, height):
            for x in range(0, width):
                pixelData[x + (y * width)] = createPixel(x, y)

            if y%(height/100) == 0:
                sys.stdout.write("-")
                sys.stdout.flush()

        sys.stdout.write("\n")
        print pixelData
        self.pixelData = pixelData

    # Render a single pixel
    def createPixel(self, x, y):

        # IMPLEMENT ANTI-ALIASING HERE, MULTIPLE RAYS PER PIXEL
        offsetX = 0.5
        offsetY = 0.5
        result = self.Tracer.startRayTrace(x + offsetX, y + offsetY)
        return [result[0], result[1], result[2], 1.0]




    # Draw Renderer
    def draw(self):
        #glRasterPos2i(-1 , -1)
        glDrawPixels(self.width , self.height , GL_RGBA , GL_FLOAT , self.pixelData)