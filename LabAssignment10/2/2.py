import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.


def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -1 , -1 , -1 ), # v7
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
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()

def slerp(R1,R2,t):
    return R1 @ exp(t * log(R1.T @ R2))
    
def exp(rv):
    
    theta = np.sqrt(rv[0]**2 + rv[1]**2 + rv[2]**2)
    
    if(theta == 0 ):
        return np.identity(3)
        
    
    else :
        vector = rv / theta
 
        result = np.array([[np.cos(theta) + vector[0]**2*(1-np.cos(theta)),vector[0] * vector[1]*(1-np.cos(theta)) - vector[2] * np.sin(theta), vector[0]* vector[2]*(1-np.cos(theta))+vector[1]*np.sin(theta)],
            [vector[1] * vector[0] * (1-np.cos(theta)) + vector[2] * np.sin(theta), np.cos(theta) + vector[1]**2*(1-np.cos(theta)), vector[1]*vector[2]*(1-np.cos(theta))- vector[0] * np.sin(theta)],
            [vector[2] * vector[0]*(1-np.cos(theta))- vector[1] * np.sin(theta), vector[2]* vector[1]*(1-np.cos(theta))+vector[0]*np.sin(theta),np.cos(theta) + vector[2]**2*(1-np.cos(theta))]])
            
    return result

def log(R):
    if(R[0,0]+R[1,1]+R[2,2] == 3):
        theta = 0
        vector = 0
    elif(R[0,0]+R[1,1]+R[2,2] == -1):
        theta = np.pi

        vector = 1/(np.sqrt(2 * (1+r[2,2])) * np.array([r[0,2],r[1,2],1+r[2,2]])) * theta
        if(vector == 0):
            vector = 1/(np.sqrt(2 * (1+r[1,1])) * np.array([r[0,1],1+r[1,1],r[2,1]]))* theta
            if(vector == 0) :
                vector = 1/(np.sqrt(2 * (1+r[0,0])) * np.array([1+r[0,0],r[1,0],1+r[2,0]])) * theta
    else :
        theta = np.arccos((R[0,0]+R[1,1]+R[2,2]-1)/2.0)
        vector = np.array([(R[2,1]-R[1,2])/(2*np.sin(theta)),(R[0,2]-R[2,0])/(2*np.sin(theta)),(R[1,0]-R[0,1])/(2*np.sin(theta))]) * theta
   
    return vector

def XYZEulerToRotMat(euler):
    xang,yang,zang = euler
    xang = np.radians(xang)
    yang = np.radians(yang)
    zang = np.radians(zang)
    
    Rx = np.array([[1,0,0],
                   [0, np.cos(xang), -np.sin(xang)],
                   [0, np.sin(xang), np.cos(xang)]])
    Ry = np.array([[np.cos(yang), 0, np.sin(yang)],
                   [0,1,0],
                   [-np.sin(yang), 0, np.cos(yang)]])
    Rz = np.array([[np.cos(zang), -np.sin(zang), 0],
                   [np.sin(zang), np.cos(zang), 0],
                   [0,0,1]])
    return Rx @ Ry @ Rz


def drawObject(t):

    euler1Matrix = XYZEulerToRotMat(np.array([20.,30.,30.]))
    euler2Matrix = XYZEulerToRotMat(np.array([15.,30.,25.]))
    euler3Matrix = XYZEulerToRotMat(np.array([45.,60.,40.]))
    euler4Matrix = XYZEulerToRotMat(np.array([25.,40.,40.]))
    euler5Matrix = XYZEulerToRotMat(np.array([60.,70.,50.]))
    euler6Matrix = XYZEulerToRotMat(np.array([40.,60.,50.]))
    euler7Matrix = XYZEulerToRotMat(np.array([80.,85.,70.]))
    euler8Matrix = XYZEulerToRotMat(np.array([55.,80.,65.]))

    R1 = np.identity(4)
    
    if 0 <= t and t < 20 :
        R1[:3,:3] = slerp(euler1Matrix,euler3Matrix,t/ 20.0)
        
    elif 20<=t and t<= 40 :
        R1[:3,:3] = slerp(euler3Matrix,euler5Matrix,(t-20)/ 20.0)
    else :
        R1[:3,:3] = slerp(euler5Matrix,euler7Matrix,(t-40)/ 20.0)

    J1 = R1
        
    glPushMatrix()
    glMultMatrixf(J1.T)

    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()


    R2 = np.identity(4)
    T1 = np.identity(4)
    T1[0][3] = 1.
        
    
    if 0<=t and t < 20 :
        R2[:3,:3] = slerp(euler2Matrix,euler4Matrix,t/ 20.0)
    elif t<=20 and t<= 40 :
        R2[:3,:3] = slerp(euler4Matrix,euler6Matrix,(t-20)/ 20.0)
    else :
        R2[:3,:3] = slerp(euler6Matrix,euler8Matrix,(t-40)/ 20.0)


    J2 = R1 @ T1 @ R2

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
        
    glPopMatrix()
    glPopMatrix()


def render(t):
    global gCamAng, gCamHeight,currentEndPoint
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
 
    

    objectColor = (1.,0,0,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    

    drawObject(0)
    
    objectColor = (1,1,0,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    drawObject(20)

    objectColor = (0,1,0,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    drawObject(40)


    objectColor = (0,0,1,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)


    drawObject(60)
 
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
  
    drawObject(t)

    glDisable(GL_LIGHTING)




def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2019016735', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    t = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render(t)

        if(t==60):
            t = 0
        else:
            t+= 1

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

