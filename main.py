#!/usr/bin/env python3
import os
import sys

import glfw
import pygame.image
from glfw.GLFW import *
from numpy import *
from OpenGL.GL import *
from OpenGL.GLU import *
from operator import mul
from objLoader import *
from pygame import *
from pynput.mouse import Listener

viewer = [0.0, 0.0, 10.0]
viewport = (1920, 1080)
tempy = 0
flag_render = False
currx = 0
curry = 0
currz = 0
move_r = 0
move_l = 0
move_u = 0
move_d = 0

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
mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]
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


def lamp(set_x, set_y, set_z, lamp_model, side):
    glColor3f(1.0, 1.0, 1.0)
    glRotate(-90, 1, 0, 0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    if side == 0:
        glRotate(-90, 0, 0, 1)
    else:
        glRotate(90, 0, 0, 1)
    glScalef(0.1, 0.1, 0.1)
    # glRotate(rx, 0, 1, 0)
    glCallList(lamp_model.gl_list)


def helipad(set_x, set_y, set_z, helipad_model):
    glColor3f(1.0, 1.0, 1.0)
    glTranslate(0, 0, 0)
    glRotate(-90, 1, 0, 0)
    glScalef(0.1, 0.1, 0.1)
    # glRotate(rx, 0, 1, 0)
    glCallList(helipad_model.gl_list)


def road(set_x, set_y, set_z, road_model):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)
    glColor3f(1.0, 1.0, 1.0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    glRotate(-90, 1, 0, 0)
    glScalef(0.2, 0.2, 0.2)
    # glRotate(rx, 0, 1, 0)
    glCallList(road_model.gl_list)


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


def building1(set_x, set_y, set_z, building1_model, side):
    glColor3f(1.0, 1.0, 1.0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    if side == 0:
        glRotate(-90, 1, 0, 0)
    else:
        glRotate(90, 1, 0, 0)
        glRotate(180, 0, 1, 0)
    glScalef(1.0, 1.0, 1.0)
    # glRotate(rx, 0, 1, 0)
    glCallList(building1_model.gl_list)


def skyscraper(set_x, set_y, set_z, building2_model):
    glColor3f(1.0, 1.0, 1.0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    glRotatef(-90, 1, 0, 0)
    # glScalef(1.0, 8.0, 8.0)
    glCallList(building2_model.gl_list)


def helicopter(set_x, set_y, set_z, heli_model):
    glColor3f(1.0, 1.0, 1.0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    glRotate(-90, 1, 0, 0)
    # glScalef(2.0, 2.0, 2.0)
    # glRotate(rx, 0, 1, 0)
    glCallList(heli_model.gl_list)


def blade(angle, set_x, set_y, set_z, blade_model):
    glColor3f(1.0, 1.0, 1.0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    glRotate(-90, 1, 0, 0)
    glScalef(1.2, 1.2, 1.2)

    glRotate(angle, 0, 0, 1)
    glCallList(blade_model.gl_list)


def set_skybox(set_x, set_y, set_z, skybox):
    glColor3f(1.0, 1.0, 1.0)
    glRotate(-90, 1, 0, 0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    glScalef(60, 60, 60)
    glCallList(skybox.gl_list)


def set_grass(set_x, set_y, set_z, grass_model):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)
    glColor3f(1.0, 1.0, 1.0)
    glRotate(90, 1, 0, 0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    #glScalef(2, 2, 2)
    glCallList(grass_model.gl_list)

# def building3(set_x,set_y,set_z,building3_model)
def road2(set_x,set_y,set_z,road_model):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)
    glColor3f(1.0, 1.0, 1.0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    glRotate(-90, 1, 0, 0)
    glRotate(-90,0,0,1)
    glScalef(0.2, 0.2, 0.2)
    # glRotate(rx, 0, 1, 0)
    glCallList(road_model.gl_list)
def building3(set_x,set_y,set_z,building3_model,rotation):
    glColor3f(1.0, 1.0, 1.0)
    glTranslate(0 + set_x, 0 + set_y, 0 + set_z)
    glRotate(-90, 1, 0, 0)
    if rotation==0:
        glRotate(90,0,0,1)
    else:
        glRotate(-90,0,0,1)
    glScalef(0.2, 0.2, 0.2)
    glCallList(building3_model.gl_list)

def render(time, x, helipad_model, road_model, lamp_model, building1_model, heli_model, blade_model, building2_model,
           skybox, grass_model,building3_model):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    global flag_render
    global tempy
    global curry
    global currx
    global currz
    mouseMove = pygame.mouse.get_rel()
    glRotatef(180 + move_r, 0.0, 1.0, 0.0)
    glRotatef(move_u, 1.0, 0.0, 0.0)
    glTranslate(0.0, -3.5, -7.5)
    if curry > -9.0:
        curry -= x
        glTranslate(0, curry, 0)
    else:
        if not flag_render:
            # tempy = -x
            flag_render = True
        currz -= x
        glTranslate(0.0, curry, currz)

    glPushMatrix()
    field(30.0, 0.0, 40.0)
    glPopMatrix()
    i = -10
    j = 0
    side = 0
    while i <= 10:
        while j < 100:
            glPushMatrix()
            if i == -10:
                if j!=48:
                    building1(i, 0, j, building1_model, 0)
            else:
                if j!=48:
                    building1(i, 0, j, building1_model, 1)
            glPopMatrix()
            j = j + 12
        i = i + 20
        j = 0

    glPushMatrix()
    helipad(0, 0, 0, helipad_model)
    glPopMatrix()
    glPushMatrix()
    skyscraper(-30, 0, 90, building2_model)
    glPopMatrix()
    y = 0
    while y > -100:
        glPushMatrix()
        road(5, 0, -y, road_model)
        glPopMatrix()
        glPushMatrix()
        road(-5, 0, -y, road_model)
        glPopMatrix()
        y -= 3.3

    y = -8.8
    while y>-100:
        glPushMatrix()
        road2(-y,0,48,road_model)
        glPopMatrix()
        glPushMatrix()
        road2(y,0,48,road_model)
        glPopMatrix()
        y-=3.3
    y=-20
    while y>-100:
        glPushMatrix()
        building3(-y,0,55,building3_model,0)
        glPopMatrix()
        glPushMatrix()
        building3(-y, 0, 41, building3_model,1)
        glPopMatrix()
        glPushMatrix()
        building3(y,0,55,building3_model,0)
        glPopMatrix()
        glPushMatrix()
        building3(y, 0, 41, building3_model,1)
        glPopMatrix()
        y-=20
    y=0
    side = 0
    count = 0
    glPushMatrix()
    generate_plachta()
    glPopMatrix()
    y = 0

    while y > -100:
        glPushMatrix()
        if side == 0:
            lamp(3, y, 0, lamp_model, 1)
            side = 1

        else:
            lamp(7, y, 0, lamp_model, 0)
            side = 0
        glPopMatrix()
        y -= 3.3
        count += 1
        y = 0

        while y > -100:
            glPushMatrix()
            if side == 0:
                lamp(3, y, 0, lamp_model, 1)
                side = 1

            else:
                lamp(7, y, 0, lamp_model, 0)
                side = 0
            glPopMatrix()
            y -= 3.3
            count += 1
        y = 0

        while y > -100:
            glPushMatrix()
            if side == 0:
                lamp(-3, y, 0, lamp_model, 0)
                side = 1

            else:
                lamp(-7, y, 0, lamp_model, 1)
                side = 0
            glPopMatrix()
            y -= 3.3
            count += 1
    glPushMatrix()
    glLight(GL_LIGHT0, GL_POSITION, (0, -curry + 1, -currz + 20, 1))
    glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 40)
    helicopter(0, -curry, -currz, heli_model)
    glPopMatrix()
    glPushMatrix()
    blade(100 * currz, 0, 6 - curry, -currz, blade_model)
    glPopMatrix()
    glPushMatrix()
    set_skybox(0.0, 0.0, 0.0, skybox)
    glPopMatrix()
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
    gluPerspective(100, width / height, 0.1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def key_callback(window, key, scancode, action, modsn):
    global move_u, move_l, move_r, move_d
    if key == glfw.KEY_UP:
        move_u += 1
        #print(move_u)
    if key == glfw.KEY_DOWN:
        move_u -= 1
        #print(move_d)
    if key == glfw.KEY_RIGHT:
        move_r += 1
        #print(move_r)
    if key == glfw.KEY_LEFT:
        move_r -= 1
        #print(move_l)


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    glfwMakeContextCurrent(window)
    glfwSetKeyCallback(window, key_callback)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)
    glEnable(GL_TEXTURE_2D)
    pygame.init()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)
    glLightf(GL_LIGHT2, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT2, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, att_quadratic)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0, 0, 0, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 30)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (0, -1, 0, 1))
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
    load_texture(1, id2)
    glActiveTexture(GL_TEXTURE2)
    load_texture(2, id3)
    glActiveTexture(GL_TEXTURE3)
    load_texture(3, id4)
    print(os.path.join(__location__,'textures\\helipad.obj'))
    helipad_model = OBJ(os.path.join(__location__, 'textures\\helipad.obj'), swapyz=True)
    road_model = OBJ(os.path.join(__location__, 'textures\\road.obj'), swapyz=True)
    lamp_model = OBJ(os.path.join(__location__, 'textures\\lamp.obj'), swapyz=True)
    building1_model = OBJ(os.path.join(__location__, 'textures\\building1.obj'), swapyz=True)
    heli_model = OBJ(os.path.join(__location__, 'textures\\heli.obj'), swapyz=True)
    blade_model = OBJ(os.path.join(__location__, 'textures\\blade.obj'), swapyz=True)
    building2_model = OBJ(os.path.join(__location__, 'textures\\building2.obj'), swapyz=True)
    skybox = OBJ(os.path.join(__location__, 'textures\\skybox.obj'), swapyz=True)
    grass = OBJ(os.path.join(__location__, 'textures\\untitled.obj'), swapyz=True)
    building3_model=OBJ(os.path.join(__location__,'textures\\Builiding3.obj'),swapyz=True)

    x = 0
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), x, helipad_model, road_model, lamp_model, building1_model, heli_model, blade_model,
               building2_model, skybox, grass,building3_model)
        x = 0.05
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
