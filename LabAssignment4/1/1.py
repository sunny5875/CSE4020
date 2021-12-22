import glfw
from OpenGL.GL import *
import numpy as np

global keyInput
keyInput=''

def render():

    
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
    
    glColor3ub(255,255,255)
    
    global keyInput
    
    for i in range(len(keyInput)-1,0,-1):
        if keyInput[i] =='Q' :
            glTranslatef(-0.1,0,0)
            
        elif keyInput[i] =='E':
            glTranslatef(0.1,0,0)
            
        elif keyInput[i] =='A':
             glRotatef(10,0,0,1)
             
        elif keyInput[i] == 'D':
            glRotatef(-10,0,0,1)
        
        else:
            break
                    

                    
    
    drawTriangle()
    
    
def drawTriangle():
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv(np.array([0.0,0.5]))
    glVertex2fv(np.array([0.0,0.0]))
    glVertex2fv(np.array([0.5,0.0]))
    glEnd()

def key_callback(window,key,scancode,action,mods):
    global keyInput

    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_Q:
            keyInput+='Q'

                    
        if key==glfw.KEY_E:
            keyInput+='E'

        if key==glfw.KEY_A:
            keyInput+='A'

         
        if key==glfw.KEY_D:
            keyInput+='D'
  
         
        if key==glfw.KEY_1:
            keyInput=''
            glLoadIdentity()
       
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
        
        
        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

