#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def generate_plachta():
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-100.0, -5.0, 100.0)
    glVertex3f(-100, -5.0, -100.0)
    glVertex3f(100.0, -5.0, 100.0)

    glVertex3f(100, -5.0, 100.0)
    glVertex3f(100, -5.0, -100.0)
    glVertex3f(-100, -5.0, -100.0)
    glEnd()


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -100.0)
    glVertex3f(0.0, 0.0, 100.0)

    glEnd()


def building(set_x, set_y, set_z):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(set_x + (-3.0), set_y + (-5.0), set_z + 0.0)
    glVertex3f(set_x + 0.0, set_y + (-5.0), set_z + 0.0)
    glVertex3f(set_x + (-3.0), set_y + -5.0, set_z + - 3.0)

    glVertex3f(set_x + 0.0, set_y + -5.0, set_z + 0.0)
    glVertex3f(set_x + -3.0, set_y + -5.0, set_z + -3.0)
    glVertex3f(set_x + 0.0, set_y + -5.0, set_z + -3.0)

    glVertex3f(set_x + -3.0, set_y + -5.0, set_z + 0.0)
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + 0.0)
    glVertex3f(set_x + 0.0, set_y + -5.0, set_z + 0.0)

    glVertex3f(set_x + 0.0, set_y + -5.0, set_z + 0.0)
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + 0.0)
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + 0.0)

    glVertex3f(set_x + -3.0, set_y + -5.0, set_z + 0.0)
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + 0.0)
    glVertex3f(set_x + -3.0, set_y + -5.0, set_z + -3.0)

    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(set_x + -3.0, set_y + -5.0, set_z + -3.0)
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + -3.0)
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + 0.0)

    glVertex3f(set_x + -3.0, set_y + -5.0, set_z + -3.0)
    glVertex3f(set_x + 0.0, set_y + -5.0, set_z + -3.0)
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + -3.0)

    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + -3.0)
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + -3.0)
    glVertex3f(set_x + 0.0, set_y + -5.0, set_z + -3.0)

    glVertex3f(set_x + 0.0, set_y + -5.0, set_z + 0.0)
    glVertex3f(set_x + 0.0, set_y + -5.0, set_z + -3.0)
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + 0.0)

    glVertex3f(set_x + 0.0, set_y + -5.0, set_z + -3.0)
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + -3.0)
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + 0.0)
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + 0.0)
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + -3.0)

    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + 0.0)
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + -3.0)
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + -3.0)

    # glVertex3f(-1.0,0.0,-3.0)
    # glVertex3f(-3.0,5.0,0.0)
    # glVertex3f(-1.0,5.0,0.0)
    # glVertex3f(-3.0,5.0,-3.0)
    # glVertex3f(-1.0,5.0,-3.0)

    glEnd()


def spin(angle):
    # glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    # glRotatef(angle, 0.0, 0.0, 1.0)


#def switch_view(x):
#    gluLookAt(x, 8.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def render(time,x):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #glFrustum(-10,10,-10,10,100,-100)
    #switch_view(x)

    # (width, height) = canvas.GetClientSize()

    # glPushMatrix()
    # spin(time * 180 / 3.1415)
    glTranslate(0,-10,0)
    glRotatef(10,1.0,0.0,0.0)
    glTranslate(0, 0,-x )
    # spin(time * 180 / 3.1415)
    # axes()
    generate_plachta()
    i=-5
    j=0
    while i<=40:
        while j<100:
            building(i,0,j)
            j=j+10
        i=i+35
        j=0
    # glTranslate(-10, 0, 5)
    # glPopMatrix()
    # building(-50.0, .0, -5.0)
    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    gluPerspective(120, width/height, 0.1, 100);
    #if width <= height:
    #    glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 100, -100)
    #else:
    #    glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 100, -100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)
    x=0
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(),x)
        x+=0.01
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
