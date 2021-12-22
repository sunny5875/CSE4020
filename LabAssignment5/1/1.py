import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gCamHeight = .1

def render():
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()


#    original version
    drawFrame()

    glColor3ub(255, 255, 255)
    drawTriangle()
    
#    rotate->translate
    glTranslatef(0.6,0,0)
    glRotatef(30,0,0,1)
    
    drawFrame()
    glColor3ub(0, 0, 255)
    drawTriangle()
    
#    translate->rotate
    glLoadIdentity()
    glRotatef(30,0,0,1)
    glTranslatef(0.6,0,0)
    
    drawFrame()
    glColor3ub(255, 0, 0)
    drawTriangle()
    
    

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glColor3ub(0, 0, 255)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,0.]))
    glEnd()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([.0,.5]))
    glVertex2fv(np.array([.0,.0]))
    glVertex2fv(np.array([.5,.0]))
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2019016735', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

