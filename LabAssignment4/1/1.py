import gc
import numpy as np
import glfw
from OpenGL.GL import *

key_input = []

def key_callback(window, key, scancode, action, mods):
    global key_input
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_Q:
            key_input.insert(0, "glTranslatef(-0.1, .0, 0)")
        elif key == glfw.KEY_E:
            key_input.insert(0, "glTranslatef(0.1, .0, 0)")
        elif key == glfw.KEY_A:
            key_input.insert(0, "glRotatef(10, 0, 0, 1)")
        elif key == glfw.KEY_D:
            key_input.insert(0, "glRotatef(-10, 0, 0, 1)")
        elif key == glfw.KEY_1:
            key_input.append("glLoadIdentity()")

def render():
    global key_input
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
    for i in range(len(key_input)):
        eval(key_input[i])
    drawTriangle()
 
def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5])) 
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(480, 480, "2016025041", None, None)
    
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
