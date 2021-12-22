import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


# draw a cube of side 1, centered at the origin.
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5)
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()

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

def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()

    myFrustum(-1,1, -1,1, 1,10)
    myLookAt(np.array([5,3,5]),np.array([1,1,-1]),np.array([0,1,0]))

#    glFrustum(-1,1,-1,1,1,10)
#    gluLookAt(5,3,5,1,1,-1,0,1,0)
    drawFrame()
    glColor3ub(255, 255, 255)

    drawCubeArray()

def myFrustum(left,right,bottom,top,near,far):
    M=np.array([[2.0*near/(right-left),.0,float(right+left)/(right-left),.0],
                [.0,2.0*near/(top-bottom),float(top+bottom)/(top-bottom),0],
                [.0,.0,-float(far+near)/(far-near),-2.0*far*near/(far-near)],
                [.0,.0,-1.,.0]])
    glMultMatrixf(M.T)

def myLookAt(eye,at,up):
    eye = eye.astype('float32')
    at = at.astype('float32')
    up = up.astype('float32')
    
    w = (eye-at)/np.sqrt(np.dot(eye-at,eye-at))
    u = np.cross(up,w)/np.sqrt(np.dot(np.cross(up,w),np.cross(up,w)))
    v = np.cross(w,u)
    
    M = np.identity(4)
    M[:3,0]=u
    M[:3,1]=v
    M[:3,2]=w
    M[:3,3]=eye
    
    M = np.linalg.inv(M)
    glMultMatrixf(M.T)


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
