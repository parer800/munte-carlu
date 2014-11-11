#!/usr/bin/python
# coding: utf-8
#render.py, Class for rendering

import numpy as np
import time
import sys
import datetime
import random as rand
import multiprocessing as mp
import types

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
        manager = mp.Manager()

        self.Tracer.init() # Init Tracer
        pixelData_Shared = manager.list([0] * (self.width * self.height))
        height = self.height
        width = self.width
        createPixel = self.createPixel
        SAMPLE_COUNT = 4

        # Creating image to store values in
        imgPixels_Shared = manager.list([0] * (self.height * self.width))

        start = time.time()

        # NUMBER OF CORES TO RUN ON
        CORE_COUNT = mp.cpu_count()
        #CORE_COUNT = 1

        pool = mp.Pool(CORE_COUNT)

        print ' '
        print 'Number of cores: ' + str(CORE_COUNT)
        print ' '

        sys.stdout.write("[%s]" % (" " * 100))
        sys.stdout.flush()
        sys.stdout.write("\b" * (100 + 1))


        
        # THREADS PARTITIONED EVEN DISTRIBUTED OVER THE IMAGE : [ abcd abcd abcd ]
        def worker(cpu, partitioning, i, p):
            y = cpu
            for row in range(0, partitioning):
                for x in range(0, width):
                    pix = createPixel(x, y, SAMPLE_COUNT)
                    #i[x][height-y-1] = (int(pix[0]*255), int(pix[1]*255), int(pix[2]*255), int(pix[3]*255))
                    i[x + ((height-y-1) * width)] = (int(pix[0]*255), int(pix[1]*255), int(pix[2]*255), int(pix[3]*255))
                    p[x + (y * width)] = pix

                if y%(height/100) == 0:
                    sys.stdout.write("-")
                    sys.stdout.flush()

                y += 4

        partitioning = height / mp.cpu_count()
        jobs = []
        for cpu in range(CORE_COUNT):
            p = mp.Process(target=worker, args=(cpu, partitioning, imgPixels_Shared, pixelData_Shared))
            p.start()
            jobs.append(p)

        for j in jobs:
            j.join()
        
        

        '''
        # THREADS PARTITIONED BY THE NUMBER OF CORES OVER THE IMAGE : [ aaa bbb ccc ddd ]
        def worker(s, e, i, p):
            for y in range(s, e):
                for x in range(0, width):
                    pix = createPixel(x, y, SAMPLE_COUNT)
                    #i[x][height-y-1] = (int(pix[0]*255), int(pix[1]*255), int(pix[2]*255), int(pix[3]*255))
                    i[x + ((height-y-1) * width)] = (int(pix[0]*255), int(pix[1]*255), int(pix[2]*255), int(pix[3]*255))
                    p[x + (y * width)] = pix

                if y%(height/100) == 0:
                    sys.stdout.write("-")
                    sys.stdout.flush()

        
        partitioning = height / mp.cpu_count()
        jobs = []
        last_cpu = 0
        for cpu in range(CORE_COUNT - 1):
            s = cpu * partitioning
            e = (cpu + 1) * partitioning
            p = mp.Process(target=worker, args=(s, e, imgPixels_Shared, pixelData_Shared))
            p.start()
            jobs.append(p)
            last_cpu = cpu + 1
        
        s = last_cpu * partitioning
        e = height
        p = mp.Process(target=worker, args=(s, e, imgPixels_Shared, pixelData_Shared))
        p.start()
        jobs.append(p)
        
        for j in jobs:
            j.join()
        '''

        
        img = Image.new( 'RGBA', (width, height))
        img.putdata(imgPixels_Shared)
        
        '''
        for y in range(0, height):
            for x in range(0, width):
                pix = createPixel(x, y, SAMPLE_COUNT)
                imgPixels[x, height-y-1] = (int(pix[0]*255), int(pix[1]*255), int(pix[2]*255), int(pix[3]*255))
                pixelData[x + (y * width)] = pix

            if y%(height/100) == 0:
                sys.stdout.write("-")
                sys.stdout.flush()
        '''

        sys.stdout.write("\n")

        end = time.time()

        timer = str(datetime.timedelta(seconds=(end - start)))
        #timer = timer[0:7]
        timer_string = str(timer).replace(":", "_")

        print ' '
        print timer
        print ' '

        img.save('../Cornell_Box_' + str(width) + 'x' + str(height) + '_' + str(SAMPLE_COUNT) + 'SPP_' + timer_string + '.png')
        self.pixelData = pixelData_Shared[:]

    # Render a single pixel
    def createPixel(self, x, y, SAMPLE_COUNT):
        
        accumulatedPixel = [0.0, 0.0, 0.0, 1.0];
        for k in range(0, SAMPLE_COUNT):
            offsetX = rand.random()
            offsetY = rand.random()
            #tracedPixel = self.Tracer.startRayTrace(x + offsetX, y + offsetY, 1.0/SAMPLE_COUNT)
            tracedPixel = self.Tracer.startRayTrace(x + offsetX, y + offsetY, 1.0)
            accumulatedPixel[0] += tracedPixel[0]
            accumulatedPixel[1] += tracedPixel[1]
            accumulatedPixel[2] += tracedPixel[2]

        #return [accumulatedPixel[0], accumulatedPixel[1], accumulatedPixel[2], 1.0]
        return [accumulatedPixel[0]/SAMPLE_COUNT, accumulatedPixel[1]/SAMPLE_COUNT, accumulatedPixel[2]/SAMPLE_COUNT, 1.0]


    # Draw Renderer
    def draw(self):
        #glRasterPos2i(-1 , -1)
        glDrawPixels(self.width , self.height , GL_RGBA , GL_FLOAT , self.pixelData)
