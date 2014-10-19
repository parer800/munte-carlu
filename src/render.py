#!/usr/bin/python
# coding: utf-8
#render.py, Class for rendering

import numpy as np
import time
import sys
import random as rand

from PIL import Image
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

        # Creating image to store values in
        img = Image.new( 'RGBA', (width,height), "black")
        imgPixels = img.load()

        sys.stdout.write("[%s]" % (" " * 100))
        sys.stdout.flush()
        sys.stdout.write("\b" * (100 + 1))

        for y in range(0, height):
            for x in range(0, width):
                pix = createPixel(x, y)
                imgPixels[x, height-y-1] = (int(pix[0]*255), int(pix[1]*255), int(pix[2]*255), int(pix[3]*255))
                pixelData[x + (y * width)] = pix

            if y%(height/100) == 0:
                sys.stdout.write("-")
                sys.stdout.flush()

        sys.stdout.write("\n")

        #img.save('../out.png')
        img.save('../Cornell_Box_' + str(width) + 'x' + str(height) + '.png')
        self.pixelData = pixelData

    # Render a single pixel
    def createPixel(self, x, y):

        SAMPLE_COUNT = 1
        
        accumulatedPixel = [0.0, 0.0, 0.0, 1.0];
        for k in range(0, SAMPLE_COUNT):
            offsetX = rand.random()
            offsetY = rand.random()
            tracedPixel = self.Tracer.startRayTrace(x + offsetX, y + offsetY)
            accumulatedPixel[0] += tracedPixel[0]
            accumulatedPixel[1] += tracedPixel[1]
            accumulatedPixel[2] += tracedPixel[2]

        return [accumulatedPixel[0]/SAMPLE_COUNT, accumulatedPixel[1]/SAMPLE_COUNT, accumulatedPixel[2]/SAMPLE_COUNT, 1.0]



    # Draw Renderer
    def draw(self):
        #glRasterPos2i(-1 , -1)
        glDrawPixels(self.width , self.height , GL_RGBA , GL_FLOAT , self.pixelData)
