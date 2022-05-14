import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import os

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
global Toggle_Projection, Perspective, Orthogonal
Toggle_Projection = True
Perspective = True
Orthogonal = False
global Toggle_Polygon, Wireframe, Solidmode
Toggle_Polygon = True
Wireframe = True
Solidmode = False
global Toggle_Shading, ShadingNormal, ForcedShading
Toggle_Shading = True
ShadingNormal = True
ForcedShading = False
global Toggle_RenderingMode, SingleMesh, AnimatingModel
Toggle_RenderingMode = True
SingleMesh = True
AnimatingModel = False
global narr, iarr, varr, fnarr, fvarr, snarr
HasPrinted = True
varr = np.empty((0, 3))
fvarr = np.empty((0, 3))
narr = np.empty((0, 3))
fnarr = np.empty((0, 3))
iarr = np.empty((0, 3))
snarr = np.empty((0, 3))
global sun_varr, sun_fvarr, sun_snarr, sun_fnarr, sun_iarr
global earth_varr, earth_fvarr, earth_snarr, earth_fnarr, earth_iarr
global moon_varr, moon_fvarr, moon_snarr, moon_fnarr, moon_iarr
global saturn_varr, saturn_fvarr, saturn_snarr, saturn_fnarr, saturn_iarr
global satellite_varr, satellite_fvarr, satellite_snarr, satellite_fnarr, satellite_iarr
global spaceship_varr, spaceship_fvarr, spaceship_snarr, spaceship_fnarr, spaceship_iarr
global naturlite_varr, naturlite_fvarr, naturlite_snarr, naturlite_fnarr, naturlite_iarr

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
        TargetPoint = TargetPoint - u * \
            (xpos - x_cursor) * 0.003 + v * (ypos - y_cursor) * 0.003


def key_callback(window, key, scancode, action, modes):
    global Toggle_Projection, Perspective, Orthogonal, Toggle_Shading, ShadingNormal, ForcedShading, Toggle_Polygon, Wireframe, Solidmode, Toggle_RenderingMode, SingleMesh, AnimatingModel
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_V:
            if Toggle_Projection == Perspective:
                Toggle_Projection = Orthogonal
            elif Toggle_Projection == Orthogonal:
                Toggle_Projection = Perspective
        if key == glfw.KEY_Z:
            if Toggle_Polygon == Wireframe:
                Toggle_Polygon = Solidmode
            elif Toggle_Polygon == Solidmode:
                Toggle_Polygon = Wireframe
        if key == glfw.KEY_S:
            if Toggle_Shading == ShadingNormal:
                Toggle_Shading = ForcedShading
            elif Toggle_Shading == ForcedShading:
                Toggle_Shading = ShadingNormal
        if key == glfw.KEY_H:
            if Toggle_RenderingMode == SingleMesh:
                Toggle_RenderingMode = AnimatingModel
            elif Toggle_RenderingMode == AnimatingModel:
                Toggle_RenderingMode = SingleMesh

def drop_callback(window, paths):
    global Toggle_RenderingMode, HasPrinted
    Toggle_RenderingMode = SingleMesh
    HasPrinted = False
    objectRender(paths[0])

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

# Draw obj with rendered arrays
def drawObject(varr, fvarr, snarr, fnarr, iarr):
    global Toggle_Shading

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    if Toggle_Shading == ForcedShading:
        if varr.size == 0: return
        glNormalPointer(GL_FLOAT, 3*snarr.itemsize, snarr)
        glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
        glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)
    elif Toggle_Shading == ShadingNormal:
        if fvarr.size == 0: return
        glNormalPointer(GL_FLOAT, 3*fnarr.itemsize, fnarr)
        glVertexPointer(3, GL_FLOAT, 3*fvarr.itemsize, fvarr)
        glDrawArrays(GL_TRIANGLES, 0, int(fvarr.size/3))
        
# Open obj file and parse, render to arrays
def objectRender(paths):
    global varr, narr, fvarr, fnarr, iarr, HasPrinted, snarr
    FaceW3vCount = 0
    FaceW4vCount = 0
    FaceW5mvCount = 0
    
    varr = np.empty((0, 3))
    fvarr = np.empty((0, 3))
    narr = np.empty((0, 3))
    fnarr = np.empty((0, 3))
    iarr = np.empty((0, 3), np.int32)
    
    f = open(paths, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        
        if len(line) == 1:
            continue
        
        t = line.split()
        line = line[2:]
        
        if (t[0] == 'v'):
            vertex = np.array([float(t[1]), float(t[2]), float(t[3])])
            # print(vertex)
            varr = np.append(varr, np.array([vertex]), axis = 0)
            
        elif (t[0] == 'vn'):
            normal = np.array([float(t[1]), float(t[2]), float(t[3])])
            # print(normal)
            narr = np.append(narr, np.array([normalize(normal)]), axis = 0)
            # print(narr)
        
        elif (t[0] == 'f'):
            if (len(t) == 4): FaceW3vCount += 1
            elif (len(t) == 5): FaceW4vCount += 1
            else: FaceW5mvCount += 1
            
            index_ = np.empty((0, 3), np.int32)
            normal_ = np.empty((0, 3), np.float32)
            
            for v in t:
                if (v == t[0]): continue
                w = v.split('/')
                index_ = np.append(index_, (int(w[0]) - 1))
                if (len(w) == 3): 
                    normal_ = np.append(normal_, [narr[int(w[2]) - 1]], axis = 0)
            
            if (len(index_) != 3):
                for i in range(2, len(index_)):
                    iarr = np.append(iarr, np.array([np.array([index_[0], index_[i - 1], index_[i]])]), axis = 0)
                    fnarr = np.append(fnarr, np.array([np.array(normal_[0]), np.array(normal_[i - 1]), np.array(normal_[i])]), axis = 0)
            else:
                iarr = np.append(iarr, np.array([index_]), axis = 0)
                for i in normal_:
                    fnarr = np.append(fnarr, np.array([i]), axis = 0)
            
    snarr = np.ones((len(varr), 3), np.float32) 

    k = 0
    for i in iarr:
        for j in i:
            # print("index : " + str(index_))
            # print("normal : " + str(normal))
            fvarr = np.append(fvarr, np.array([varr[j]]), axis = 0)
            snarr[j] += fnarr[k]
            k += 1
            
    for i in range(len(varr)):
        # print(snarr[i])
        if (np.sqrt(snarr[i] @ snarr[i]) != 0):
            snarr[i] = normalize(snarr[i])
        
    varr = varr.astype(np.float32)
    fvarr = fvarr.astype(np.float32)
    snarr = snarr.astype(np.float32)
    fnarr = fnarr.astype(np.float32)
                    
    if HasPrinted == False & SingleMesh:
        print("File name : " +  paths.split('/')[-1])
        print("Total number of faces : " + str(FaceW3vCount + FaceW4vCount + FaceW5mvCount))
        print("Number of faces with 3 vertices : " + str(FaceW3vCount))
        print("Number of faces with 4 vertices : " + str(FaceW4vCount))
        print("Number of faces with more than 4 vertices : ", str(FaceW5mvCount))
        HasPrinted = True
    
    return varr, fvarr, snarr, fnarr, iarr
                
def normalize(v):
    return np.array(v) / np.sqrt(v @ v)

# Animate Hierarchical Model
def drawAnimatingModel():
    global sun_varr, sun_fvarr, sun_snarr, sun_fnarr, sun_iarr
    global earth_varr, earth_fvarr, earth_snarr, earth_fnarr, earth_iarr
    global moon_varr, moon_fvarr, moon_snarr, moon_fnarr, moon_iarr
    global saturn_varr, saturn_fvarr, saturn_snarr, saturn_fnarr, saturn_iarr
    global satellite_varr, satellite_fvarr, satellite_snarr, satellite_fnarr, satellite_iarr
    global spaceship_varr, spaceship_fvarr, spaceship_snarr, spaceship_fnarr, spaceship_iarr
    global naturlite_varr, naturlite_fvarr, naturlite_snarr, naturlite_fnarr, naturlite_iarr
    
    t = glfw.get_time()

    # Sun Transform
    glPushMatrix()
    glRotatef(t*(180/np.pi), 0, 1, 0)
    
    # Sun Drawing
    glPushMatrix()
    objectColor = (1, 0, 0, 1)
    specularColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glScalef(4, 4, 4)
    drawObject(sun_varr, sun_fvarr, sun_snarr, sun_fnarr, sun_iarr)
    glPopMatrix()
    
    # Earth Transform
    glPushMatrix()
    glRotatef(t*(180/np.pi), -1, 1, 0)
    glTranslatef(5., 5., 5.)
    
    # Earth Drawing
    glPushMatrix()
    objectColor = (0, 0, 1, 1)
    specularColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glScalef(.5, .5, .5)
    drawObject(earth_varr, earth_fvarr, earth_snarr, earth_fnarr, earth_iarr)
    glPopMatrix()
    
    # Satellite Transform
    glPushMatrix()
    glRotatef(2*t*(180/np.pi), 1, -1, 0)
    glTranslatef(1., 1., .1)
    
    # Satellite Drawing
    glPushMatrix()
    objectColor = (.1, .1, .1, 1)
    specularColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glScalef(.05, .05, .05)
    drawObject(satellite_varr, satellite_fvarr, satellite_snarr, satellite_fnarr, satellite_iarr)
    glPopMatrix()
    glPopMatrix()
    
    # Moon Transform
    glPushMatrix()
    glRotatef(0.6*t*(180/np.pi), 1, 0, 1)
    glTranslatef(-1.5, 1.5, 1.5)
    
    # Moon Drawing
    glPushMatrix()
    objectColor = (.01, .01, .01, 1)
    specularColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glScalef(.3, .3, .3)
    drawObject(moon_varr, moon_fvarr, moon_snarr, moon_fnarr, moon_iarr)
    glPopMatrix() 
    glPopMatrix()
    glPopMatrix()
    
    # Saturn Transform
    glPushMatrix()
    glRotatef(t*(180/np.pi), 0, 1, 0)
    glTranslatef(20., 0., 20.)
    glRotatef(15, 1, 0, 1)
    
    # Saturn Drawing
    glPushMatrix()
    objectColor = (.12, .12, .12, 1)
    specularColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glScalef(3, 3, 3)
    drawObject(saturn_varr, saturn_fvarr, saturn_snarr, saturn_fnarr, saturn_iarr)
    glPopMatrix()
    
    # Spaceship Transform
    glPushMatrix()
    glRotate(1.3*t*(180/np.pi), 0, 0, 0)
    glTranslatef(3.7, 4., 3.9)
    
    # Spaceship Drawing 
    glPushMatrix()
    objectColor = (.8, .9, .7, 1)
    specularColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glScalef(1., 1., 1.)
    drawObject(spaceship_varr, spaceship_fvarr, spaceship_snarr, spaceship_fnarr, spaceship_iarr)
    glPopMatrix()
    glPopMatrix()
    
    # Natural Satellite Transform
    glPushMatrix()
    glRotatef(1.5*t*(180/np.pi), 1, 1, 0)
    glTranslatef(5., -5., -5.)
    
    # Natural Satellite Drawing
    glPushMatrix()
    objectColor = (.8, .9, .7, 1)
    specularColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glScalef(.03, .03, .03)
    drawObject(naturlite_varr, naturlite_fvarr, naturlite_snarr, naturlite_fnarr, naturlite_iarr)
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def render():
    global ArimuthAngle, ElevationAngle, u, v, w, EyePoint, TargetPoint, UpVector, varr, fvarr, snarr, fnarr, iarr
    global Toggle_Polygon, Toggle_Projection, Toggle_RenderingMode
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    # Toggle Polygonmode
    if Toggle_Polygon == Wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    elif Toggle_Polygon == Solidmode:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glLoadIdentity()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Toggle Projection
    if Toggle_Projection == Perspective:
        gluPerspective(45, 1, 1, 200)
    elif Toggle_Projection == Orthogonal:
        glOrtho(-0.5*Distance, 0.5*Distance, -0.5 *
                Distance, 0.5*Distance, -100, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Calculate coordinate of camera and its vectors
    ArimuteRadian = np.radians(ArimuthAngle)
    ElevationRadian = np.radians(ElevationAngle)
    EyePoint = np.array([Distance * np.cos(ElevationRadian) * np.cos(ArimuteRadian) + TargetPoint[0],
                         Distance * np.sin(ElevationRadian) + TargetPoint[1],
                         Distance * np.sin(ArimuteRadian) * np.cos(ElevationRadian) + TargetPoint[2]])
    w = (EyePoint - TargetPoint) / \
        np.sqrt((EyePoint - TargetPoint) @ (EyePoint - TargetPoint))
    u = np.cross(UpVector, w) / \
        np.sqrt(np.cross(UpVector, w) @ np.cross(UpVector, w))
    v = np.cross(w, u)

    gluLookAt(EyePoint[0], EyePoint[1], EyePoint[2],
              TargetPoint[0], TargetPoint[1], TargetPoint[2],
              UpVector[0], UpVector[1], UpVector[2])

    drawFrame()
    drawRectangularGrid()

    # Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_NORMALIZE)

    lightPos0 = (10., 10., 10., 1.)
    lightColor0 = (1., 0., 0., 1.)
    ambientLightColor0 = (.1, .0, .0, 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor0)

    lightPos1 = (-10., 10., 10., 1.)
    lightColor1 = (0., 1., 0., 1.)
    ambientLightColor1 = (.0, .1, .0, 1.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor1)

    lightPos2 = (10., 10., -10., 1.)
    lightColor2 = (0., 0., 1., 1.)
    ambientLightColor2 = (.0, .0, .1, 1.)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor2)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor2)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor2)

    objectColor = (.5, .5, .5, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    # Object Rendering
    if Toggle_RenderingMode == SingleMesh:
        drawObject(varr, fvarr, snarr, fnarr, iarr)
    elif Toggle_RenderingMode == AnimatingModel:
        drawAnimatingModel()

    glDisable(GL_LIGHTING)

def main():
    global varr, fvarr, snarr, fnarr, iarr
    global sun_varr, sun_fvarr, sun_snarr, sun_fnarr, sun_iarr
    global earth_varr, earth_fvarr, earth_snarr, earth_fnarr, earth_iarr
    global moon_varr, moon_fvarr, moon_snarr, moon_fnarr, moon_iarr
    global saturn_varr, saturn_fvarr, saturn_snarr, saturn_fnarr, saturn_iarr
    global satellite_varr, satellite_fvarr, satellite_snarr, satellite_fnarr, satellite_iarr
    global spaceship_varr, spaceship_fvarr, spaceship_snarr, spaceship_fnarr, spaceship_iarr
    global naturlite_varr, naturlite_fvarr, naturlite_snarr, naturlite_fnarr, naturlite_iarr
    
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Basic OpenGL viewer", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)
    
    # Prepare for Hierarchical Model
    path_sun = os.path.join(".", "Sun.obj")
    sun_varr, sun_fvarr, sun_snarr, sun_fnarr, sun_iarr = objectRender(path_sun)
    path_earth = os.path.join(".", "Earth.obj")
    earth_varr, earth_fvarr, earth_snarr, earth_fnarr, earth_iarr = objectRender(path_earth)
    path_moon = os.path.join(".", "Moon.obj")
    moon_varr, moon_fvarr, moon_snarr, moon_fnarr, moon_iarr = objectRender(path_moon)
    path_saturn = os.path.join(".", "Saturn.obj")
    saturn_varr, saturn_fvarr, saturn_snarr, saturn_fnarr, saturn_iarr = objectRender(path_saturn)
    path_satellite = os.path.join(".", "Satellite2.obj")
    satellite_varr, satellite_fvarr, satellite_snarr, satellite_fnarr, satellite_iarr = objectRender(path_satellite)
    path_spaceship = os.path.join(".", "Spaceship.obj")
    spaceship_varr, spaceship_fvarr, spaceship_snarr, spaceship_fnarr, spaceship_iarr = objectRender(path_spaceship)
    path_naturlite = os.path.join(".", "Natural_Satellite.obj")
    naturlite_varr, naturlite_fvarr, naturlite_snarr, naturlite_fnarr, naturlite_iarr = objectRender(path_naturlite)
    
    # Initialize Vectors for Object File Render
    varr = np.empty((0, 3))
    fvarr = np.empty((0, 3))
    narr = np.empty((0, 3))
    fnarr = np.empty((0, 3))
    iarr = np.empty((0, 3), np.int32)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()