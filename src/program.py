#!/usr/bin/python
# coding: utf-8

from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL.Image import open

width = 800
height = 600

rgbdata = ''
for x in range(0, width):
    for y in range(0, height):
        rgbdata += 'a'
        rgbdata += '0'
        rgbdata += '0'

print rgbdata


def draw():
    glClearColor(1.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRasterPos2i(-1 , -1);
    glDrawPixels(width , height , GL_RGB , GL_UNSIGNED_BYTE , rgbdata);
    glFlush()
    glutSwapBuffers()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutCreateWindow("Munte Carlu")
glutDisplayFunc(draw)
glutMainLoop()