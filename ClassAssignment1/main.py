import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


zoom = 5

xPos = 0
yPos = 0

oldxPos = 0
oldyPos = 0

right = False
left = False
isPerspective= True

gElevation = np.radians(36.264)
gAzimuth = np.radians(45.)
upVector = np.array([0.,1.,0.])

center = np.array([0.,0.,0.])

global gVertexArrayIndexed, gIndexArray
global M,u,v,w

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
    
def drawUnitCube():
    glBegin(GL_QUADS)
    glColor3ub(255, 255, 255)
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

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            (-5,0,5),(-4,0,5),(-3,0,5),(-2,0,5),(-1,0,5),(0,0,5),(1,0,5),
            (2,0,5),(3,0,5),(4,0,5),(5,0,5),(5,0,4),(5,0,3),(5,0,2),
            (5,0,1),(5,0,0),(5,0,-1),(5,0,-2),(5,0,-3),(5,0,-4),(5,0,-5),
                
            (4,0,-5),(3,0,-5),(2,0,-5),(1,0,-5),(0,0,-5),(-1,0,-5),(-2,0,-5),
            (-3,0,-5),(-4,0,-5),(-5,0,-5),(-5,0,-4),(-5,0,-3),(-5,0,-2),(-5,0,-1),
            (-5,0,0),(-5,0,1),(-5,0,2),(-5,0,3),(-5,0,4)
            
            ], 'float32')
    iarr = np.array([(0,10),(20,30),
            (0,30),(1,29),(2,28),(3,27),(4,26),(5,25),(6,24),(7,23),(8,22),(9,21),(10,20),
            (11,39),(12,38),(13,37),(14,36),(15,35),(16,34),(17,33),(18,32),(19,31),(20,30)
            ])
    return varr, iarr

    
def drawGrid():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_LINES, iarr.size, GL_UNSIGNED_INT, iarr)


def myLookAt():
    global zoom,center,gAzimuth,gElevation,upVector,M,u,v,w
    
#calculate camera's coordinate system
    w = np.array([np.cos(gElevation) * np.sin(gAzimuth), np.sin(gElevation),np.cos(gElevation)*np.cos(gAzimuth)])

    w=w/np.sqrt(np.dot(w,w))

    u = np.cross(upVector,w)
    u = u / np.sqrt(np.dot(u,u))

    v = np.cross(w,u)
    v = v / np.sqrt(np.dot(v,v))

#get viewing transformation
    M = np.identity(4)
    M[:3,0]=u
    M[:3,1]=v
    M[:3,2]=w
    M[:3,3]=w*zoom + center

    M = np.linalg.inv(M)


    

def render():
    global isPerspective,M,zoom,center,gAzimuth,gElevation,upVector
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

    glLoadIdentity()
  

#  check perspective /ortho
    if(isPerspective == True):
        gluPerspective(45, 1, 1,10)
    else :
        glOrtho (-2.5,2.5,-2.5,2.5,-10,10)
    
    
    myLookAt()
    glMultMatrixf(M.T)
#    gluLookAt(zoom * w[0] + center[0], zoom * w[1]+center[1],zoom*w[2]+center[2],
#    center[0],center[1],center[2],upVector[0],upVector[1],upVector[2])

    drawFrame()
    glColor3ub(128, 128, 128)
    drawGrid()
    glColor3ub(255, 255, 255)
    drawUnitCube()
    
    


def cursor_callback(window, xpos,ypos):
    global oldxPos,oldyPos,xPos,yPos,right,left,gAzimuth,gElevation,center,u,v
    
    oldxPos=xPos
    oldyPos=yPos
    
    xPos=xpos
    yPos=ypos
#    orbit
    if(left == True):
        gAzimuth+=np.radians(-xPos+oldxPos)
        gElevation+=np.radians(-yPos+oldyPos)
        
        if np.cos(gElevation) < 0:
            upVector = -1.
        else:
            upVector = 1.
#    panning
    if(right == True):
        center= center +((+oldxPos-xPos)* u + (-oldyPos+yPos)* v)*0.01
        
        
    
  

def mouse_button_callback(window, button, action, mods):
    global right,left
    if button == glfw.MOUSE_BUTTON_LEFT:
        if( action == glfw.PRESS):
                left = True
        elif action == glfw.RELEASE :
            left = False
    if button == glfw.MOUSE_BUTTON_RIGHT:
        if( action == glfw.PRESS):
                right = True
        elif action == glfw.RELEASE :
            right = False

    
#zooming
def scroll_callback(window, xoffset, yoffset):
    global zoom

    zoom+=yoffset*(-0.1)

#perspective & ortho
def key_callback(window,key,scancode, action, mods):
    global isPerspective
    if key == glfw.KEY_V :
        if action == glfw.PRESS or action == glfw.REPEAT:
            isPerspective= not isPerspective

    
        

   


def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(1000,1000,'ClassAssignment', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window,scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_key_callback(window,key_callback)
   
    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
    myLookAt()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

