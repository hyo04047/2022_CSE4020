import numpy as np
from OpenGL.GLU import *
from OpenGL.GL import *
import glfw

zoom = 5

xPos = 0
yPos = 0

oldxPos = 0
oldyPos = 0

right = False
left = False
isPerspective = True

gElevation = np.radians(36.264)
gAzimuth = np.radians(45.)
upVector = np.array([0., 1., 0.])

center = np.array([0., 0., 0.])

global gVertexArrayIndexed, gIndexArray
global M, u, v, w
global path
isDrag = False

global varr, iarr, narr, smoothNarr, varr_
global earthNarr, earthVarr, moonNarr, moonVarr, sunNarr, sunVarr, backGroundNarr, backGroundVarr
global earthSmoothNarr, earthVarr_, moonVarr_, moonSmoothNarr, sunVarr_, sunSmoothNarr, backGroundVarr_, backGroundSmoothNarr, earthIarr, moonIarr, sunIarr, backgroundIarr

isHierarchicalMode = False
iswireframeMode = True
isSmmothShading = False
isFirst = True


# draw coordinate
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

# grid varr, iarr


def createVertexAndIndexArrayIndexed():
    varr = np.array([
        (-5, 0, 5), (-4, 0, 5), (-3, 0, 5), (-2,
                                             0, 5), (-1, 0, 5), (0, 0, 5), (1, 0, 5),
        (2, 0, 5), (3, 0, 5), (4, 0, 5), (5, 0,
                                          5), (5, 0, 4), (5, 0, 3), (5, 0, 2),
        (5, 0, 1), (5, 0, 0), (5, 0, -1), (5, 0, -
                                           2), (5, 0, -3), (5, 0, -4), (5, 0, -5),

        (4, 0, -5), (3, 0, -5), (2, 0, -5), (1, 0, -
                                             5), (0, 0, -5), (-1, 0, -5), (-2, 0, -5),
        (-3, 0, -5), (-4, 0, -5), (-5, 0, -5), (-5,
                                                0, -4), (-5, 0, -3), (-5, 0, -2), (-5, 0, -1),
        (-5, 0, 0), (-5, 0, 1), (-5, 0, 2), (-5, 0, 3), (-5, 0, 4)

    ], 'float32')
    iarr = np.array([(0, 10), (20, 30),
                     (0, 30), (1, 29), (2, 28), (3, 27), (4, 26), (5,
                                                                   25), (6, 24), (7, 23), (8, 22), (9, 21), (10, 20),
                     (11, 39), (12, 38), (13, 37), (14, 36), (15,
                                                              35), (16, 34), (17, 33), (18, 32), (19, 31), (20, 30)
                     ])
    return varr, iarr


def drawGrid():
    global gVertexArrayIndexed, gIndexArray
    glPushMatrix()
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_LINES, iarr.size, GL_UNSIGNED_INT, iarr)
    glPopMatrix()


def myLookAt():
    global zoom, center, gAzimuth, gElevation, upVector, M, u, v, w

#   calculate camera's coordinate system
    w = np.array([np.cos(gElevation) * np.sin(gAzimuth),
                 np.sin(gElevation), np.cos(gElevation)*np.cos(gAzimuth)])

    w = w/np.sqrt(np.dot(w, w))

    u = np.cross(upVector, w)
    u = u / np.sqrt(np.dot(u, u))

    v = np.cross(w, u)
    v = v / np.sqrt(np.dot(v, v))

#   get viewing transformation
    M = np.identity(4)
    M[:3, 0] = u
    M[:3, 1] = v
    M[:3, 2] = w
    M[:3, 3] = w*zoom + center

    M = np.linalg.inv(M)

#hierarchical model


def drawHierarchicalModel():
    global earthNarr, earthVarr, moonNarr, moonVarr, sunNarr, sunVarr, backGroundVarr, backGroundNarr, earthSmoothNarr, earthVarr_, moonVarr_, moonSmoothNarr, sunVarr_, sunSmoothNarr, backGroundVarr_, backGroundSmoothNarr, earthIarr, moonIarr, sunIarr, backgroundIarr
    t = glfw.get_time()

#   background
    glPushMatrix()
    glTranslatef(0.8, 2.3, 0.3)
    glScalef(0.03, 0.03, 0.03)
    drawObject(backGroundNarr, backGroundVarr, backGroundSmoothNarr,
               backGroundVarr_, backgroundIarr)
    glScalef(-1, -1, 1)
    glTranslatef(100, 200, 50)
    drawObject(backGroundNarr, backGroundVarr, backGroundSmoothNarr,
               backGroundVarr_, backgroundIarr)
    glPopMatrix()

#    sun
    glPushMatrix()
    glScalef(1+np.abs(np.sin(t)/10.0), 1 +
             np.abs(np.sin(t)/10.0), 1+np.abs(np.sin(t)/10.0))
    glRotatef(t*(180/np.pi), 0, 1, 0)

    glPushMatrix()
    glScalef(0.009, 0.009, 0.009)

    glPushMatrix()
    glScalef(100, 100, 100)
    glPushMatrix()
    drawObject(sunNarr, sunVarr, sunSmoothNarr, sunVarr_, sunIarr)
    glPopMatrix()
    glPopMatrix()

#    earth
    glPushMatrix()
    glRotatef(t*(180/np.pi), 0, 1, 0)
    glPushMatrix()
    glTranslate(100, 100, 40)
    glScalef(10, 10, 10)
    glPushMatrix()
    glRotatef(t*(180/np.pi), 0, 1, 0)
    drawObject(earthNarr, earthVarr, earthSmoothNarr, earthVarr_, earthIarr)
    glPopMatrix()

#   moon
    glPushMatrix()
    glRotatef(2*t*(180/np.pi), 0, 1, 0)

    glPushMatrix()
    glTranslate(2, 0, 2)
    glScalef(.007, .007, .007)
#    glScalef(1000,1000,1000)
    glRotatef(2*t*(180/np.pi), 0, 1, 0)
    drawObject(moonNarr, moonVarr, moonSmoothNarr, moonVarr_, moonIarr)

    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()


def render():
    global isPerspective, M, zoom, center, gAzimuth, gElevation, upVector, isDrag, iswireframeMode, isHierarchicalMode, narr, varr, smoothNarr, varr_

#    wireframe mode
    if (iswireframeMode == True):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


#  check perspective /ortho
    if(isPerspective == True):
        gluPerspective(45, 1, 1, 10)
    else:
        glOrtho(-2.5, 2.5, -2.5, 2.5, -10, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    myLookAt()
    glMultMatrixf(M.T)
#    gluLookAt(zoom * w[0] + center[0], zoom * w[1]+center[1],zoom*w[2]+center[2],
#    center[0],center[1],center[2],upVector[0],upVector[1],upVector[2])

    glDisable(GL_LIGHTING)
    drawFrame()
    glColor3ub(128, 128, 128)
    drawGrid()
    glColor3ub(255, 255, 255)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_NORMALIZE)

    glPushMatrix()

#    light color1
    lightPos = (3., 4., 5., 1.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    # light intensity for each color channel
    lightColor = (1., 0., 0., 1.)
    ambientLightColor = (.1, .0, .0, 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    glPushMatrix()

#    light color2
    lightPos = (5., 4., 3., 1.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()

    # light intensity for each color channel
    lightColor = (0., 1., 0., 1.)
    ambientLightColor = (.0, .1, 0., 1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

    glPushMatrix()

#    light color3
    lightPos = (3., -5., 3., 1.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT3, GL_POSITION, lightPos)
    glPopMatrix()

    # light intensity for each color channel
    lightColor = (0., 0., 1., 1.)
    ambientLightColor = (.0, .0, .1, 1.)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT3, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT3, GL_AMBIENT, ambientLightColor)

    # material reflectance for each color channel
    objectColor = (.8, .8, .8, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    if(isDrag == True and isHierarchicalMode == False):
        drawObject(narr, varr, smoothNarr, varr_, iarr)

    if(isHierarchicalMode == True):
        drawHierarchicalModel()

    glDisable(GL_LIGHTING)


# make vector's size 1
def normalized(v):
    l = np.sqrt(np.dot(v, v))
    return 1/l * np.array(v)


# obj parser and calculate varr,narr,smoothNarr,varr_,iarr
def singleMeshRendering():
    global varr, iarr, file, narr, path, isFirst, isDrag, isSmmothShading, smoothNarr, varr_
#    drag and drop file
    if(isDrag == True):
        file = open(str(path)[2:-2], 'r')
    else:  # hierarchical mode file
        file = open(path, 'r')


#    initialize
    varr = np.empty((0, 3), float)
    iarr = np.empty((0, 3), np.int32)
    narr = np.empty((0, 3), float)
    narr_ = np.empty((0, 3), float)
    varr_ = np.empty((0, 3), float)


#    count face
    face3Count = 0
    face4Count = 0
    faceMoreThan4Count = 0

    while True:
        line = file.readline()

        if not line:
            break

#    remove blank line
        if len(line) == 1:
            continue

        line = line.replace("\n", "")
        splitLine = line.split()
        line = line[2:]

#        f parsing
        if splitLine[0] == 'f':
            if(len(splitLine) == 4):
                face3Count += 1
            elif(len(splitLine) == 5):
                face4Count += 1
            else:
                faceMoreThan4Count += 1

            index = np.empty((0, 3), np.int32)
            item = np.empty((0, 3), np.float32)

            for word in splitLine:
                if(word == splitLine[0]):
                    continue

                v = word.split('/')

                index = np.append(index, (int(v[0])-1))

                if len(v) == 3:
                    item = np.append(item, [narr_[int(v[2])-1]], axis=0)


#    triangluration
            if(len(index) != 3):
                index1 = np.array([index[0], index[1], index[2]])
                index2 = np.array([index[0], index[2], index[3]])
                for i in range(2, len(index)):
                    temp_index = np.array([index[0], index[i-1], index[i]])
                    iarr = np.append(iarr, np.array([temp_index]), axis=0)

                    temp_item = np.array(
                        [np.array(item[0]), np.array(item[i-1]), np.array(item[i])])
                    narr = np.append(narr, temp_item, axis=0)
            else:
                iarr = np.append(iarr, np.array([index]), axis=0)
                for i in item:
                    narr = np.append(narr, np.array([i]), axis=0)


#   vn parsing
        elif splitLine[0] == 'vn':
            item = normalized([float(splitLine[1]), float(
                splitLine[2]), float(splitLine[3])])
            narr_ = np.append(narr_, np.array([item]), axis=0)

#    v parsing
        elif splitLine[0] == 'v':

            item = np.array(
                [[float(splitLine[1]), float(splitLine[2]), float(splitLine[3])]])
            varr_ = np.append(varr_, item, axis=0)


#    normalCountArr = np.zeros((len(varr_),),float)
    smoothNarr = np.zeros((len(varr_), 3), float)
    j = 0
    for index in iarr:
        for item in index:
          #            normalCountArr[item] += 1
            # print("index : " + str(index))
            # print("normal : " + str(item))
            varr = np.append(varr, np.array([varr_[item]]), axis=0)
            smoothNarr[item] += narr[j]
            j += 1


#   calculate smoothNarr
    for i in range(len(varr_)):
        print(smoothNarr[i])
      #        smoothNarr[i] /= np.full((3,),float(normalCountArr[i]))
        smoothNarr[i] = normalized(smoothNarr[i])

    if isFirst == False:
        print("file name : " + str(path))
        print("total number of faces : " + str(len(iarr)))
        print("number of faces with 3 vertices : " + str(face3Count))
        print("number of faces with 4 vertices : " + str(face4Count))
        print("number of faces with  more than 4 vertices : " +
              str(faceMoreThan4Count))

    varr = varr.astype(np.float32)
#    iarr= varr.astype(np.int32)
    narr = narr.astype(np.float32)
    varr_ = varr_.astype(np.float32)
    smoothNarr = smoothNarr.astype(np.float32)

    return narr, varr, smoothNarr, varr_, iarr


def drawObject(narr, varr, smoothNarr, varr_, iarr):
    global isSmmothShading

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

#   force smooth shading
    if(isSmmothShading == True):
        glNormalPointer(GL_FLOAT, 3*smoothNarr.itemsize, smoothNarr)
        glVertexPointer(3, GL_FLOAT, 3*varr_.itemsize, varr_)
        glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

#  flat shading
    else:
        glNormalPointer(GL_FLOAT, 3*narr.itemsize, narr)
        glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
        glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 3))


def cursor_callback(window, xpos, ypos):
    global oldxPos, oldyPos, xPos, yPos, right, left, gAzimuth, gElevation, center, u, v

    oldxPos = xPos
    oldyPos = yPos

    xPos = xpos
    yPos = ypos
#    orbit
    if(left == True):
        gAzimuth += np.radians(-xPos+oldxPos)
        gElevation += np.radians(-yPos+oldyPos)

        if np.cos(gElevation) < 0:
            upVector = -1.
        else:
            upVector = 1.
#    panning
    if(right == True):
        center = center + ((+oldxPos-xPos) * u + (-oldyPos+yPos) * v)*0.01


def mouse_button_callback(window, button, action, mods):
    global right, left
    if button == glfw.MOUSE_BUTTON_LEFT:
        if(action == glfw.PRESS):
            left = True
        elif action == glfw.RELEASE:
            left = False
    if button == glfw.MOUSE_BUTTON_RIGHT:
        if(action == glfw.PRESS):
            right = True
        elif action == glfw.RELEASE:
            right = False


#zooming
def scroll_callback(window, xoffset, yoffset):
    global zoom

    zoom += yoffset*(-0.1)

#perspective & ortho


def key_callback(window, key, scancode, action, mods):
    global isPerspective, isHierarchicalMode, iswireframeMode, isSmmothShading
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_V:
            isPerspective = not isPerspective
        if key == glfw.KEY_H:
            isHierarchicalMode = True
        if key == glfw.KEY_Z:
            iswireframeMode = not iswireframeMode
        if key == glfw.KEY_S:
            isSmmothShading = not isSmmothShading


#drag and drop
def fileparse(window, paths):
    global isDrag, isHierarchicalMode, path
    path = paths
    isDrag = True
    singleMeshRendering()
    isHierarchicalMode = False


def main():
    global gVertexArrayIndexed, gIndexArray, path, earthNarr, earthVarr, moonNarr, moonVarr, sunNarr, sunVarr, isFirst, backGroundNarr, backGroundVarr, earthSmoothNarr, earthVarr_, moonVarr_, moonSmoothNarr, sunVarr_, sunSmoothNarr, backGroundVarr_, backGroundSmoothNarr, earthIarr, moonIarr, sunIarr, backgroundIarr
    if not glfw.init():
        return
    window = glfw.create_window(700, 700, 'ClassAssignment2', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, fileparse)

    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
    myLookAt()

# #    loading hiearichal mode
#     path = 'earth.obj'
#     earthNarr, earthVarr, earthSmoothNarr, earthVarr_, earthIarr = singleMeshRendering()

#     path = 'moon.obj'
#     moonNarr, moonVarr, moonSmoothNarr, moonVarr_, moonIarr = singleMeshRendering()

#     path = 'sun.obj'
#     sunNarr, sunVarr, sunSmoothNarr, sunVarr_, sunIarr = singleMeshRendering()

#     path = 'background.obj'
#     backGroundNarr, backGroundVarr, backGroundSmoothNarr, backGroundVarr_, backgroundIarr = singleMeshRendering()

    isFirst = False

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()