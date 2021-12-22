###################################################
# [Practice] OpenGL Lighting
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gCamAng = 0.
gCamHeight = 1.

red=0.
green=0.
blue=0.

global glVertexArrayIndexed,glIndexArray

def createVertexArraySeparate():
    varr = np.array([
            (-0.5773502691896258,0.5773502691896258,0.5773502691896258),         # v0 normal
            ( -1 ,  1 ,  1 ), # v0 position
            (0.8164965809277261,0.4082482904638631,0.4082482904638631),         # v2 normal
            (  1 , 1 ,  1 ), # v2 position
            (0.4082482904638631,-0.4082482904638631,0.8164965809277261),         # v1 normal
            (  1 ,  -1 ,  1 ), # v1 position

            (-0.4082482904638631,-0.8164965809277261,0.4082482904638631),         # v0 normal
            ( -1 ,  -1 ,  1 ), # v0 position
            (-0.4082482904638631,0.4082482904638631,-0.8164965809277261),         # v3 normal
            ( -1 , 1 ,  -1 ), # v3 position
            (0.4082482904638631,0.8164965809277261,-0.4082482904638631),         # v2 normal
            (  1 , 1 ,  -1 ), # v2 position

            (0.5773502691896258,-0.5773502691896258,-0.5773502691896258),
            ( 1 ,  -1 , -1 ), # v4
            (-0.8164965809277261,-0.4082482904638631,-0.4082482904638631),
            (  -1 ,  -1 , -1 ), # v5
          
            ], 'float32')
            
    iarr = np.array([
    (0,2,1),
    (0,3,2),
    (4,5,6),
    (4,6,7),
    (0,1,5),
    (0,5,4),
    (3,6,2),
    (3,7,6),
    (1,2,6),
    (1,6,5),
    (0,7,3),
    (0,4,7)
    ])
    return varr,iarr

def drawCube_glDrawElements():
    global glVertexArrayIndexed,glIndexArray
    varr = glVertexArrayIndexed
    iarr = glIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT,6*4,varr)
    glVertexPointer(3,GL_FLOAT,6*4,ctypes.c_void_p(varr.ctypes.data+3*4))
    glDrawElements(GL_TRIANGLES,36,GL_UNSIGNED_INT,iarr)
    

def render():
    global gCamAng, gCamHeight,red,green,blue
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_NORMALIZE)

    # light position
    glPushMatrix()

    t = glfw.get_time()

    # glRotatef(t*(180/np.pi),0,1,0)  # try to uncomment: rotate light
    lightPos = (3.,4.,5.,1.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    # light intensity for each color channel
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    # material reflectance for each color channel
    objectColor = (red,green,blue,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    drawCube_glDrawElements()
    
    glPopMatrix()

    glDisable(GL_LIGHTING)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight,red,green,blue
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_R:
            red=1-red
        elif key==glfw.KEY_G:
            green=1-green
        elif key==glfw.KEY_B:
            blue=1-blue

gVertexArraySeparate = None
def main():
    global glVertexArrayIndexed,glIndexArray

    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2019016735', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    glVertexArrayIndexed,glIndexArray = createVertexArraySeparate()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()


