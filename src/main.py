#!/usr/bin/python
# coding: utf-8
# main.py, Main file: run by pyhton main.py

from OpenGL.GL import *
from OpenGL.GLUT import *
from render import *

WINDOW_WIDTH = 5
WINDOW_HEIGHT = 5
Renderer = Render(WINDOW_WIDTH, WINDOW_HEIGHT)

# Init Main
def init():
	Renderer.init() # Init Renderer
	
# Draw Main
def draw():
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	glEnable( GL_BLEND );
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	Renderer.draw() # Draw Renderer
	glFlush()
	glutSwapBuffers()


init() # Init Main
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow("Munte Carlu: A Monte Carlo Ray Tracer")
glutDisplayFunc(draw) # Draw
glutMainLoop()