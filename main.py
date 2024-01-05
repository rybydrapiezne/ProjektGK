#!/usr/bin/env python3
import sys

import pygame.image
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame import *

viewer = [0.0, 0.0, 10.0]

textureSurface = pygame.image.load('/Users/vhsz/Downloads/djim-loic-Sq7WPOjHGDs-unsplash.jpg'), pygame.image.load(
    '/Users/vhsz/Downloads/photos_2021_4_6_fst_wall-rough-gray_InVaY0P.jpg'),pygame.image.load('/Users/vhsz/Downloads/fussballfeld_03_c.jpg')
textureDat = (pygame.image.tostring(textureSurface[0], "RGBA"), pygame.image.tostring(textureSurface[1], "RGBA"),
              pygame.image.tostring(textureSurface[2],"RGBA"))

width = textureSurface[0].get_width(), textureSurface[1].get_width(),textureSurface[2].get_width()
height = textureSurface[0].get_height(), textureSurface[1].get_height(),textureSurface[2].get_height()
vertices_texture = (
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0),
)
building2_vertices = (
    (-10.0, 0.0, 0.0),#podloga
    (0.0, 0.0, 0.0),
    (-10.0, 0.0, -15.0),
    (-10.0, 0.0, -15.0),
    (0.0, 0.0, 0.0),
    (0.0, 0.0, -15.0),#koniec podlogi
    (-10.0,0.0,0.0),#sciana lewa
    (-10.0,4.0,0.0),
    (-10.0,0.0,-15.0),
    (-10.0,0.0,-15.0),
    (-10.0,4.0,-15.0),
    (-10.0,4.0,0.0),# koniec sciany lewej
    (-10.0,0.0,0.0),#sciana przednia
    (0.0,0.0,0.0),
    (-10.0,4.0,0.0),
    (0.0,0.0,0.0),
    (0.0,4.0,0.0),
    (-10.0,4.0,0.0),#koniec sciany przedniej
    (0.0,0.0,0.0),#sciana prawa
    (0.0,4.0,0.0),
    (0.0,0.0,-15.0),
    (0.0,0.0,-15.0),
    (0.0,4.0,-15.0),
    (0.0,4.0,0.0),#koniec sciany prawej
    (-10.0,0.0,-15.0),#sciana tylnia
    (0.0,0.0,-15.0),
    (-10.0,4.0,-15.0),
    (-10.0,4.0,-15.0),
    (0.0,4.0,-15.0),
    (0.0,0.0,-15.0),#koniec sciany tylniej

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
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width[file], height[file], 0, GL_RGBA, GL_UNSIGNED_BYTE, textureDat[file])

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


def building2(set_x, set_y, set_z):
    glColor3f(1.0, 1.0, 1.0)
    first=0
    second=0
    third=0
    glBegin(GL_TRIANGLES)
    # podloga
    for sides in building2_vertices:
        for x, vertex in enumerate(sides):
            if x==0:
                first=vertex
            if x==1:
                second=vertex
            if x==2:
                third=vertex
        #TODO zmiana na quads bo nie poradzimy sobie z oteksutowaniem nie recznym
        glVertex3f(set_x+first,set_y+second,set_z+third)
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


def render(time, x):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # glFrustum(-10,10,-10,10,100,-100)
    # switch_view(x)

    # (width, height) = canvas.GetClientSize()

    # glPushMatrix()
    # spin(time * 180 / 3.1415)'
    glTranslate(0, -10, 0)
    glRotatef(10, 1.0, 0.0, 0.0)
    glTranslate(0, 0, -x)

    # spin(time * 180 / 3.1415)
    # axes()
    generate_plachta()
    building2(-4.0, 0.0, 0.0)
    i = -20
    j = 0
    while i <= 20:
        while j < 100:
            building(i, 0, j)
            j = j + 5
        i = i + 40
        j = 0
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
    id = glGenTextures(1)
    id2 = glGenTextures(1)
    id3=glGenTextures(1)
    glActiveTexture(GL_TEXTURE0)
    load_texture(0, id)
    glActiveTexture(GL_TEXTURE1)
    # glActiveTexture(GL_TEXTURE1)
    load_texture(1, id2)
    glActiveTexture(GL_TEXTURE2)
    load_texture(2,id3)
    x = 0
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), x)
        x += 0.01
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
