import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

global LeftMouse, RightMouse
LeftMouse = False
RightMouse = False
global ArimuthAngle, ElevationAngle
ArimuthAngle = 45
ElevationAngle = 30
global u, v, w
global EyePoint, TargetPoint, UpVector, Distance
TargetPoint = np.array([0., 0., 0.])
UpVector = np.array([0., 1., 0.])
Distance = 25
global x_cursor, y_cursor
global toggle, Perspective, Orthogonal
Toggle = True
Perspective = True
Orthogonal = False

def mouse_button_callback(window, button, action, mods):
    global LeftMouse, RightMouse, x_cursor, y_cursor
    if action == glfw.PRESS or action == glfw.REPEAT:
        if button == glfw.MOUSE_BUTTON_LEFT:
            LeftMouse = True
            x_cursor, y_cursor = glfw.get_cursor_pos(window)
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            RightMouse = True
            x_cursor, y_cursor = glfw.get_cursor_pos(window)
    elif action == glfw.RELEASE:
        LeftMouse = False
        RightMouse = False
        
def scroll_callback(window, xoffset, yoffset):
    global Distance
    # Zoom
    Distance -= yoffset
    if Distance < 1:
        Distance = 1
    
def cursor_callback(window, xpos, ypos):
    global ArimuthAngle, ElevationAngle, UpVector, LeftMouse, RightMouse, x_cursor, y_cursor, u, v, w, TargetPoint
    # Orbit
    if LeftMouse == True and RightMouse == False:
        ArimuthAngle += 0.003 * (xpos - x_cursor)
        ElevationAngle += 0.003 * (ypos - y_cursor)
    # Pan
    elif LeftMouse == False and RightMouse == True:
        TargetPoint = TargetPoint - u * (xpos - x_cursor) * 0.003 + v * (ypos - y_cursor) * 0.003
        
def key_callback(window, key, scancode, action, modes):
    global Toggle, Perspective, Orthogonal
    if action == glfw.PRESS and key == glfw.KEY_V:
        if Toggle == Perspective:
            Toggle = Orthogonal
        elif Toggle == Orthogonal:
            Toggle = Perspective

# Draw x,y,z axis
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

# Draw a rectangular grid with lines on xz plane
def drawRectangularGrid():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    for i in range(-100, 100 + 1):
        glVertex3fv(np.array([i, 0, 100]))
        glVertex3fv(np.array([i, 0, -100]))
        glVertex3fv(np.array([100, 0, i]))
        glVertex3fv(np.array([-100, 0, i]))
    glEnd()

def render():
    global ArimuthAngle, ElevationAngle, u, v, w, EyePoint, TargetPoint, UpVector
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    glLoadIdentity()
    
    # Toggle Projection
    if Toggle == Perspective:
        gluPerspective(45, 1, 1, 200)
    elif Toggle == Orthogonal:
        glOrtho(-0.5*Distance, 0.5*Distance, -0.5*Distance, 0.5*Distance, -100, 100)
    
    # Calculate coordinate of camera and its vectors
    ArimuteRadian = np.radians(ArimuthAngle)
    ElevationRadian = np.radians(ElevationAngle) 
    EyePoint = np.array([Distance * np.cos(ElevationRadian) * np.cos(ArimuteRadian) + TargetPoint[0],
                         Distance * np.sin(ElevationRadian) + TargetPoint[1],
                         Distance * np.sin(ArimuteRadian) * np.cos(ElevationRadian) + TargetPoint[2]])
    w = (EyePoint - TargetPoint) / np.sqrt((EyePoint - TargetPoint) @ (EyePoint - TargetPoint))
    u = np.cross(UpVector, w) / np.sqrt(np.cross(UpVector, w) @ np.cross(UpVector, w))
    v = np.cross(w, u)
    
    gluLookAt(EyePoint[0], EyePoint[1], EyePoint[2], 
              TargetPoint[0], TargetPoint[1], TargetPoint[2], 
              UpVector[0], UpVector[1], UpVector[2])
    
    drawFrame()
    drawRectangularGrid()

def main():
    if not glfw.init():
        return

    window = glfw.create_window(960, 600, "Basic OpenGL viewer", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()