#!/usr/bin/env python3
import os
import sys

import pygame.image
from glfw.GLFW import *
from numpy import *
from OpenGL.GL import *
from OpenGL.GLU import *
from operator import mul
from objLoader import *
from pygame import *

viewer = [0.0, 0.0, 10.0]
viewport = (1920, 1080)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
textureSurface = pygame.image.load(os.path.join(__location__, 'wall.jpg')), pygame.image.load(
    os.path.join(__location__, 'side_wall.jpg')), pygame.image.load(os.path.join(__location__, 'football_field.jpg')), \
                 pygame.image.load(os.path.join(__location__, 'fence.png'))

textureDat = (pygame.image.tostring(textureSurface[0], "RGBA"), pygame.image.tostring(textureSurface[1], "RGBA"),
              pygame.image.tostring(textureSurface[2], "RGBA"), pygame.image.tostring(textureSurface[3], "RGBA"))

width = textureSurface[0].get_width(), textureSurface[1].get_width(), textureSurface[2].get_width(), \
        textureSurface[3].get_width()
height = textureSurface[0].get_height(), textureSurface[1].get_height(), textureSurface[2].get_height(), \
         textureSurface[3].get_height()
vertices_texture = (
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0),
)
field_vertices = (
    (-10.0, 0.0, 0.0),  # podloga
    (0.0, 0.0, 0.0),
    (0.0, 0.0, -7.0),
    (-10.0, 0.0, -7.0),  # koniec podlogi
    (-10.0, 0.0, -7.0),  # sciana lewa
    (-10.0, 0.0, 0.0),
    (-10.0, 1.0, 0.0),
    (-10.0, 1.0, -7.0),  # koniec sciany lewej
    (-10.0, 0.0, 0.0),  # sciana przednia
    (0.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (-10.0, 1.0, 0.0),  # koniec sciany przedniej
    (0.0, 0.0, 0.0),  # sciana prawa
    (0.0, 0.0, -7.0),
    (0.0, 1.0, -7.0),
    (0.0, 1.0, 0.0),  # koniec sciany prawej
    (0.0, 0.0, -7.0),  # sciana tylnia
    (-10.0, 0.0, -7.0),
    (-10.0, 1.0, -7.0),
    (0.0, 1.0, -7.0),  # koniec sciany tylniej

)
helipad_vertices = (
    (0.0, 0.1, 0.0),
    (10.0, 0.1, 0.0),
    (10.0, 0.1, 10.0),
    (0.0, 0.1, 10.0),
)
theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
global tekstura2


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def load_texture(file, id_curr):
    glBindTexture(GL_TEXTURE_2D, id_curr)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width[file], height[file], 0, GL_RGBA, GL_UNSIGNED_BYTE, textureDat[file])

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)


def generate_plachta():
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-100.0, -0.001, 100.0)
    glVertex3f(-100, -0.001, -100.0)
    glVertex3f(100.0, -0.001, 100.0)

    glVertex3f(100, -0.001, 100.0)
    glVertex3f(100, -0.001, -100.0)
    glVertex3f(-100, -0.001, -100.0)
    glEnd()


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -100.0)
    glVertex3f(0.0, 0.0, 100.0)

    glEnd()


def helipad(set_x, set_y, set_z,helipad_model):
    glColor3f(1.0,1.0,1.0)
    glTranslate(0, 0, 0)
    glRotate(-90, 1,0, 0)
    glScalef(0.1,0.1,0.1)
    #glRotate(rx, 0, 1, 0)
    glCallList(helipad_model.gl_list)



def field(set_x, set_y, set_z):
    glColor3f(1.0, 1.0, 1.0)
    first = 0
    second = 0
    third = 0
    text = 0
    flag = 0
    multiply = (1.0, 1.0)
    curr = 0
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, 3)
    glBegin(GL_QUADS)
    for sides in field_vertices:
        if text > 3:
            text = 0
        for x, vertex in enumerate(sides):

            if x == 0:
                first = vertex
            if x == 1:
                second = vertex
            if x == 2:
                third = vertex
        glTexCoord2fv(tuple(map(mul, vertices_texture[text], multiply)))
        glVertex3f(set_x + first, set_y + second, set_z + third)
        if text == 3 and flag == 0:
            glEnd()
            # FragColo
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, 4)
            multiply = (3.0, 0.5)
            glBegin(GL_QUADS)
            flag = 1
        text += 1
    glEnd()


def building(set_x, set_y, set_z):
    glColor3f(1, 1, 1)
    # id = glGenTextures(1)
    # glBindTexture(GL_TEXTURE_2D, id)
    glActiveTexture(GL_TEXTURE0)
    # load_texture(0, id)
    # glActiveTexture(GL_TEXTURE1)
    # load_texture(1,id2)
    # glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 1)
    # glActiveTexture(GL_TEXTURE1)
    glBegin(GL_TRIANGLES)
    # sciany
    glColor3f(1.0, 1.0, 1.0)
    glTexCoord2fv(vertices_texture[1])
    glVertex3f(set_x + -3.0, set_y + 0.0, set_z + 0.0)
    glTexCoord2fv(vertices_texture[2])
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + 0.0)
    glTexCoord2fv(vertices_texture[0])
    glVertex3f(set_x + -3.0, set_y + 0.0, set_z + -3.0)

    glTexCoord2fv(vertices_texture[0])
    glVertex3f(set_x + -3.0, set_y + 0.0, set_z + -3.0)
    glTexCoord2fv(vertices_texture[3])
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + -3.0)
    glTexCoord2fv(vertices_texture[2])
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + 0.0)

    glColor3f(1.0, 1.0, 1.0)
    glTexCoord2fv(vertices_texture[0])
    glVertex3f(set_x + (-3.0), set_y + 0.0, set_z + 0.0)
    glTexCoord2fv(vertices_texture[1])
    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + 0.0)
    glTexCoord2fv(vertices_texture[2])
    glVertex3f(set_x + (-3.0), set_y + 0.0, set_z + - 3.0)

    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + 0.0)
    glVertex3f(set_x + -3.0, set_y + 0.0, set_z + -3.0)
    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + -3.0)

    glTexCoord2fv(vertices_texture[0])
    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + 0.0)
    glTexCoord2fv(vertices_texture[1])
    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + -3.0)
    glTexCoord2fv(vertices_texture[3])
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + 0.0)

    glTexCoord2fv(vertices_texture[1])
    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + -3.0)
    glTexCoord2fv(vertices_texture[2])
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + -3.0)
    glTexCoord2fv(vertices_texture[3])
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + 0.0)
    glEnd()

    # mała sciana
    # glDisable(GL_TEXTURE_2D)
    # glEnable(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, 2)
    # glActiveTexture(GL_TEXTURE1)
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    glTexCoord2fv(vertices_texture[0])
    glVertex3f(set_x + -3.0, set_y + 0.0, set_z + 0.0)
    glTexCoord2fv(vertices_texture[1])
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + 0.0)
    glTexCoord2fv(vertices_texture[3])
    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + 0.0)

    glTexCoord2fv(vertices_texture[3])
    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + 0.0)
    glTexCoord2fv(vertices_texture[2])
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + 0.0)
    glTexCoord2fv(vertices_texture[1])
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + 0.0)

    # glColor3f(0.0, 1.0, 1.0)
    glTexCoord2fv(vertices_texture[0])
    glVertex3f(set_x + -3.0, set_y + 0.0, set_z + -3.0)
    glTexCoord2fv(vertices_texture[3])
    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + -3.0)
    glTexCoord2fv(vertices_texture[1])
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + -3.0)

    glTexCoord2fv(vertices_texture[1])
    glVertex3f(set_x + -3.0, set_y + 6.0, set_z + -3.0)
    glTexCoord2fv(vertices_texture[2])
    glVertex3f(set_x + 0.0, set_y + 6.0, set_z + -3.0)
    glTexCoord2fv(vertices_texture[3])
    glVertex3f(set_x + 0.0, set_y + 0.0, set_z + -3.0)

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


# def switch_view(x):
#    gluLookAt(x, 8.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def render(time, x,helipad_model):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # glFrustum(-10,10,-10,10,100,-100)
    # switch_view(x)

    # (width, height) = canvas.GetClientSize()

    # glPushMatrix()
    # spin(time * 180 / 3.1415)'

    glTranslate(0.0, -1.0, 0.0)
    glRotatef(10, 1.0, 0.0, 0.0)
    glTranslate(0, -x, -x)

    # spin(time * 180 / 3.1415)
    # axes()
    generate_plachta()
    field(-4.0, 0.0, 0.0)
    i = -20
    j = 0
    while i <= 20:
        while j < 100:
            building(i, 0, j)
            j = j + 5
        i = i + 40
        j = 0
    helipad(0, 0, 0, helipad_model)

    # glTranslate(-10, 0, 5)
    # glPopMatrix()
    # building00.0, .0,0.0)
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
    gluPerspective(120, width / height, 0.1, 100)
    # if width <= height:
    #    glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 100, -100)
    # else:
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
    glEnable(GL_TEXTURE_2D)
    pygame.init()
    # srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
    glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    id = glGenTextures(1)
    id2 = glGenTextures(1)
    id3 = glGenTextures(1)
    id4 = glGenTextures(1)
    glActiveTexture(GL_TEXTURE0)
    load_texture(0, id)
    glActiveTexture(GL_TEXTURE1)
    # glActiveTexture(GL_TEXTURE1)
    load_texture(1, id2)
    glActiveTexture(GL_TEXTURE2)
    load_texture(2, id3)
    glActiveTexture(GL_TEXTURE3)
    load_texture(3, id4)
    helipad_model = OBJ( os.path.join(__location__, 'helipad.obj'), swapyz=True)

    x = 0
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), x,helipad_model)
        x += 0.01
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
