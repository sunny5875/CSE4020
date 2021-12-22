import glfw
from OpenGL.GL import *
import numpy as np

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

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2019016735", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        t = glfw.get_time()

        c= np.cos(t)
        s = np.sin(t)
        M = np.array([[c,-s,0],
                      [s,c,0],
                      [0.,0.,1]])
        S= np.array([[1,0,0.3],
                    [0,1,0.3],
                    [0,0,1]])
        
        render(M@S)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
