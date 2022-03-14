import numpy as np
import glfw
from OpenGL.GL import *

#D
global v

def render():
    global v
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(v)
    #B,C
    glVertex2f(0.5,0.5)
    glVertex2f(-0.5,0.5)
    glVertex2f(-0.5,-0.5)
    glVertex2f(0.5,-0.5)
    glEnd()

#E
def key_callback(window, key, scancode, action, mods):
    global v
    if action==glfw.PRESS:
        if key==glfw.KEY_1:
            v = GL_POINTS
        elif key==glfw.KEY_2:
            v = GL_LINES
        elif key==glfw.KEY_3:
            v = GL_LINE_STRIP
        elif key==glfw.KEY_4:
            v = GL_LINE_LOOP
        elif key==glfw.KEY_5:
            v = GL_TRIANGLES
        elif key==glfw.KEY_6:
            v = GL_TRIANGLE_STRIP
        elif key==glfw.KEY_7:
            v = GL_TRIANGLE_FAN
        elif key==glfw.KEY_8:
            v = GL_QUADS
        elif key==glfw.KEY_9:
            v = GL_QUAD_STRIP
        elif key==glfw.KEY_0:
            v = GL_POLYGON

def main():
    if not glfw.init():
        return
    #A
    window = glfw.create_window(480,480,"2016025041",None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
   
    glfw.terminate()
    
if __name__ == "__main__":
    v = GL_LINE_LOOP
    main()