import glfw
from OpenGL.GL import *
import numpy as np

global gComposedM
gComposedM=np.identity(3)

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw coordinate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((T @ np.array([0.0,0.5,1.]))[:-1])
    glVertex2fv((T @ np.array([0.0,0.0,1.]))[:-1])
    glVertex2fv((T @ np.array([0.5,0.0,1.]))[:-1])
    glEnd()

def key_callback(window,key,scancode,action,mods):
    global gComposedM
    global M
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_W:
            M=np.array([[1,0,0],
                    [0,.9,0],
                    [0,0,1]])
                    
        if key==glfw.KEY_E:
            M=np.array([[1,0,0],
                    [0,1.1,0],
                    [0,0,1]])
        if key==glfw.KEY_S:
            c=np.cos((10)*(np.pi/180))
            s=np.sin((10)*(np.pi/180))
            M=np.array([[c,-s,0],
                    [s,c,0],
                    [0,0,1]])
        if key==glfw.KEY_D:
            c=np.cos((-10)*(np.pi/180))
            s=np.sin((-10)*(np.pi/180))
            M=np.array([[c,-s,0],
                    [s,c,0],
                    [0,0,1]])
        if key==glfw.KEY_X:
            M=np.array([[1,0,.1],
                    [0,1,0],
                    [0,0,1]])
        if key==glfw.KEY_C:
            M=np.array([[1,0,-.1],
                    [0,1,0],
                    [0,0,1]])
        if key==glfw.KEY_R:
            M=np.array([[-1,0,0],
                    [0,-1,0],
                    [0,0,1]])
        if key==glfw.KEY_1:
            M=np.identity(3)
            gComposedM=np.identity(3)
            
        gComposedM= M @ gComposedM
    else:
        pass



def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2019016735", None,None)
    if not window:
        glfw.terminate()
        return
        
    glfw.set_key_callback(window,key_callback)
    
    glfw.make_context_current(window)
  

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        
        render(gComposedM)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
