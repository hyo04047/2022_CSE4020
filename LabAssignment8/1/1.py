import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *
import ctypes

gCamAng = 45
gCamHeight = 1.1

lightColor = (1., 1., 1., 1.)
objectColor = (1., 1., 1., 1.)

def createVertexAndIndexArrayIndexed():
    varr = np.array([
        (0, 0, 1),
        (-1, 1, 1),
        (0, 0, 1),
        (1, -1, 1),
        (0, 0, 1),
        (1, 1, 1),
        
        (0, 0, 1),
        (-1, 1, 1),
        (0, 0, 1),
        (-1, -1, 1),
        (0, 0, 1),
        (1, -1, 1),

        (0, 0, -1),
        (-1,  1, -1),
        (0, 0, -1),
        (1,  1, -1),
        (0, 0, -1),
        (1, -1, -1),

        (0, 0, -1),
        (-1,  1, -1),
        (0, 0, -1),
        (1, -1, -1),
        (0, 0, -1),
        (-1, -1, -1),

        (0, 1, 0),
        (-1, 1, 1),
        (0, 1, 0),
        (1, 1, 1),
        (0, 1, 0),
        (1, 1, -1),

        (0, 1, 0),
        (-1, 1, 1),
        (0, 1, 0),
        (1, 1, -1),
        (0, 1, 0),
        (-1, 1, -1),

        (0, -1, 0),
        (-1, -1, 1),
        (0, -1, 0),
        (1, -1, -1),
        (0, -1, 0),
        (1, -1, 1),

        (0, -1, 0),
        (-1, -1, 1),
        (0, -1, 0),
        (-1, -1, -1),
        (0, -1, 0),
        (1, -1, -1),

        (1, 0, 0),
        (1, 1, 1),
        (1, 0, 0),
        (1, -1, 1),
        (1, 0, 0),
        (1, -1, -1),

        (1, 0, 0),
        (1, 1, 1),
        (1, 0, 0),
        (1, -1, -1),
        (1, 0, 0),
        (1, 1, -1),

        (-1, 0, 0),
        (-1, 1, 1),
        (-1, 0, 0),
        (-1, -1, -1),
        (-1, 0, 0),
        (-1, -1, 1),

        (-1, 0, 0),
        (-1, 1, 1),
        (-1, 0, 0),
        (-1, 1, -1),
        (-1, 0, 0),
        (-1, -1, -1),
    ], 'float32')
    
    return varr

def render():
    global gCamAng, gCamHeight, objectColor
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    glLoadIdentity()
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 10)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng), gCamHeight, 5 *
              np.cos(gCamAng), 0, 0, 0, 0, 1, 0)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    
    lightPos = (3., 4., 5., 1.)
    ambientLightColor = (.1, .1, .1, 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    drawFrame()
    glColor3ub(255, 255, 255)
    drawCube_glDrawElements()
    glDisable(GL_LIGHTING)

def drawCube_glDrawElements():
    global gVertexArrayIndexed
    varr = gVertexArrayIndexed
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize,
                    ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 6))


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, lightColor, objectColor
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key == glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key == glfw.KEY_2:
            gCamHeight += .1
        elif key == glfw.KEY_W:
            gCamHeight += -.1
        elif key == glfw.KEY_A:
            lightColor = (1., 0., 0., 1.)
        elif key == glfw.KEY_S:
            lightColor = (0., 1., 0., 1.)
        elif key == glfw.KEY_D:
            lightColor = (0., 0., 1., 1.)
        elif key == glfw.KEY_F:
            lightColor = (1., 1., 1., 1.)
        elif key == glfw.KEY_Z:
            objectColor = (1., 0., 0., 1.)
        elif key == glfw.KEY_X:
            objectColor = (0., 1., 0., 1.)
        elif key == glfw.KEY_C:
            objectColor = (0., 0., 1., 1.)
        elif key == glfw.KEY_V:
            objectColor = (1., 1., 1., 1.)

gVertexArrayIndexed = None
gIndexArray = None


def main():
    global gVertexArrayIndexed, gIndexArray

    if not glfw.init():
        return
    window = glfw.create_window(480, 480, '2016025041', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    gVertexArrayIndexed = createVertexAndIndexArrayIndexed()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
