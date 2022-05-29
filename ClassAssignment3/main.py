from traceback import print_tb
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
Distance = 10
global x_cursor, y_cursor
global Toggle_Projection, Perspective, Orthogonal
Toggle_Projection = True
Perspective = True
Orthogonal = False
global Toggle_Polygon, Wireframe, Solidmode
Toggle_Polygon = False
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
global Toggle_bvhRenderingMode, LineRendering, BoxRendering
Toggle_bvhRenderingMode = True
LineRendering = True
BoxRendering = False
global bvh, starttime, bvhAnimate, isbvhcreated, motions
bvhAnimate = False
isbvhcreated = False
motions = []
global isObj
isObj = False


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
    global Toggle_Projection, Perspective, Orthogonal, Toggle_Shading, ShadingNormal, ForcedShading, Toggle_Polygon, Wireframe, Solidmode, Toggle_RenderingMode, SingleMesh, AnimatingModel, Toggle_bvhRenderingMode, LineRendering, BoxRendering, starttime, bvhAnimate
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
        if key == glfw.KEY_1:
            Toggle_bvhRenderingMode = LineRendering;
        if key == glfw.KEY_2:
            Toggle_bvhRenderingMode = BoxRendering;
        if key == glfw.KEY_SPACE:
            bvhAnimate = not bvhAnimate
            starttime = glfw.get_time()


def drop_callback(window, paths):
    # global Toggle_RenderingMode, HasPrinted
    # Toggle_RenderingMode = SingleMesh
    global HasPrinted, isbvhcreated
    HasPrinted = False
    isbvhcreated = False
    bvhRender(paths[0])
    # objectRender(paths[0])

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
        if varr.size == 0:
            return
        glNormalPointer(GL_FLOAT, 3*snarr.itemsize, snarr)
        glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
        glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)
    elif Toggle_Shading == ShadingNormal:
        if fvarr.size == 0:
            return
        glNormalPointer(GL_FLOAT, 3*fnarr.itemsize, fnarr)
        glVertexPointer(3, GL_FLOAT, 3*fvarr.itemsize, fvarr)
        glDrawArrays(GL_TRIANGLES, 0, int(fvarr.size/3))
        

def createVertexArraySeparate():
    varr = np.array([
        [0, 1, 0],            # v0 normal
        [0.5, 0, -0.5],   # v0 position
        [0, 1, 0],            # v1 normal
        [-0.5, 0, -0.5],   # v1 position
        [0, 1, 0],            # v2 normal
        [-0.5, 0, 0.5],   # v2 position

        [0, 1, 0],            # v3 normal
        [0.5, 0, -0.5],   # v3 position
        [0, 1, 0],            # v4 normal
        [-0.5, 0, 0.5],   # v4 position
        [0, 1, 0],            # v5 normal
        [0.5, 0, 0.5],   # v5 position

        [0, -1, 0],           # v6 normal
        [0.5, -1, 0.5],   # v6 position
        [0, -1, 0],           # v7 normal
        [-0.5, -1, 0.5],   # v7 position
        [0, -1, 0],           # v8 normal
        [-0.5, -1, -0.5],   # v8 position

        [0, -1, 0],
        [0.5, -1, 0.5],
        [0, -1, 0],
        [-0.5, -1, -0.5],
        [0, -1, 0],
        [0.5, -1, -0.5],

        [0, 0, 1],
        [0.5, 0, 0.5],
        [0, 0, 1],
        [-0.5, 0, 0.5],
        [0, 0, 1],
        [-0.5, -1, 0.5],

        [0, 0, 1],
        [0.5, 0, 0.5],
        [0, 0, 1],
        [-0.5, -1, 0.5],
        [0, 0, 1],
        [0.5, -1, 0.5],

        [0, 0, -1],
        [0.5, -1, -0.5],
        [0, 0, -1],
        [-0.5, -1, -0.5],
        [0, 0, -1],
        [-0.5, 0, -0.5],

        [0, 0, -1],
        [0.5, -1, -0.5],
        [0, 0, -1],
        [-0.5, 0, -0.5],
        [0, 0, -1],
        [0.5, 0, -0.5],

        [-1, 0, 0],
        [-0.5, 0, 0.5],
        [-1, 0, 0],
        [-0.5, 0, -0.5],
        [-1, 0, 0],
        [-0.5, -1, -0.5],

        [-1, 0, 0],
        [-0.5, 0, 0.5],
        [-1, 0, 0],
        [-0.5, -1, -0.5],
        [-1, 0, 0],
        [-0.5, -1, 0.5],

        [1, 0, 0],
        [0.5, 0, -0.5],
        [1, 0, 0],
        [0.5, 0, 0.5],
        [1, 0, 0],
        [0.5, -1, 0.5],

        [1, 0, 0],
        [0.5, 0, -0.5],
        [1, 0, 0],
        [0.5, -1, 0.5],
        [1, 0, 0],
        [0.5, -1, -0.5],
        # ...
    ], 'float32')
    return varr


def drawUnitCube_glDrawArray():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize,
                    ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))


class Bvh:
    def __init__(self, name):
        self.name = name
        self.joint = {}
        self.rootJoint = None
        self.frames = 0
        self.fps = 0
    
    def parsebvhFile(self, paths):
        global motions
        f = open(paths, 'r')
        file = f.read()
        hieararchy, motion = file.split("MOTION")
        
        lines = hieararchy.split('\n')
        joints = []
        idx = 0
        for line in lines:
            line = line.strip()
            word = line.split(' ')
            if word[0] == 'JOINT' or word[0] == 'ROOT':
                if word[0] == 'JOINT':
                    parent = joints[-1]
                    joint = Joint(word[1], [], parent)
                    parent.addChild(joint)
                    joints.append(joint)
                    self.joint[joint.name] = joint
                    
                if word[0] == 'ROOT':
                    joint = Joint(word[1], [], None)
                    self.rootJoint = joint
                    joints.append(joint)
                    self.joint[joint.name] = joint
                    
            elif word[0] == 'CHANNELS':
                for i in range(0, int(word[1])):
                    joints[-1].motionidx.append(idx)
                    idx += 1
                    joints[-1].channel.append(word[2 + i])
                    
            elif word[0] == 'OFFSET':
                for i in range(1, len(word)):
                    joints[-1].offset[i - 1] = float(word[i])
                    
            elif word[0] == 'End':
                joint = Joint(joints[-1].name, [], joints[-1])
                joints[-1].addChild(joint)
                joints.append(joint)
                # self.joint[joint.name] = joint
                
            elif word[0] == '}':
                joints.pop()
        
        lines = motion.split('\n')
        for line in lines:
            if line == '':
                continue
            if line.startswith('Frames:'):
                self.frames = int(line.split(' ')[1])
                continue
            if line.startswith('Frame'):
                line.split(' ')
                self.fps = 1 / float(line.split(' ')[2])
                continue
            line = line.replace('\n', '')
            line = line.strip()
            line = line.replace('\t', " ")
            line = line.split()
            line = list(map(float, line))
            motions.append(line)
                
    def printInfo(self):
        print("File name : " + self.name)
        print("Number of frames :" + str(self.frames)+" frames")
        print("FPS : " + str(self.fps))
        print("Number of joints : " + str(len(self.joint.keys())) + " joints")
        print("List of all joint names : ")
        for i in self.joint.keys():
            print(i)
            
    def drawbvh(self):
        glPushMatrix()
        if self.name == 'shoot.bvh' or self.name == 'jump.bvh':
            glScalef(.02, .02, .02)
        self.rootJoint.drawJoint()
        glPopMatrix()
            
    def animatebvh(self):
        global starttime
        glPushMatrix()
        curtime = glfw.get_time() - starttime
        frame = int(curtime * self.fps) % self.frames
        if self.name == 'shoot.bvh' or self.name == 'jump.bvh':
            glScalef(.02, .02, .02)
        self.rootJoint.animateJoint(frame)
        glPopMatrix()
    
    def setArr(self):
        self.joint['Head'].arr.append(parseOBJ('head.obj'))
        self.joint['Spine'].arr.append(parseOBJ('spine.obj'))
        self.joint['RightArm'].arr.append(parseOBJ('rightarm.obj'))
        self.joint['RightForeArm'].arr.append(parseOBJ('rightforearm.obj'))
        self.joint['RightHand'].arr.append(parseOBJ('righthand.obj'))
        self.joint['LeftArm'].arr.append(parseOBJ('leftarm.obj'))
        self.joint['LeftForeArm'].arr.append(parseOBJ('leftforearm.obj'))
        self.joint['LeftHand'].arr.append(parseOBJ('lefthand.obj'))
        self.joint['RightUpLeg'].arr.append(parseOBJ('rightupleg.obj'))
        self.joint['RightLeg'].arr.append(parseOBJ('rightleg.obj'))
        self.joint['RightFoot'].arr.append(parseOBJ('rightfoot.obj'))
        self.joint['LeftUpLeg'].arr.append(parseOBJ('leftupleg.obj'))
        self.joint['LeftLeg'].arr.append(parseOBJ('leftleg.obj'))
        self.joint['LeftFoot'].arr.append(parseOBJ('leftfoot.obj'))
                    
            
class Joint:
    def __init__(self, name, chan, parent):
        self.name = name
        self.parent = parent
        self.child = []
        self.arr = []
        self.offset = np.zeros(3)
        self.channel = chan
        self.motionidx = []
    
    def addChild(self, child):
        self.child.append(child)
        
    def drawJoint(self):
        global Toggle_bvhRenderingMode, BoxRendering, LineRendering
        glPushMatrix()
        glTranslatef(self.offset[0], self.offset[1], self.offset[2])
        glColor3ub(150, 150, 255)
        for child in self.child:
            if isObj:
                drawObj(child.offset, child.arr)
            else:
                if Toggle_bvhRenderingMode == LineRendering:
                    if self.parent:
                        glBegin(GL_LINES)
                        glVertex3fv(-self.offset)
                        glVertex3fv(np.array([0, 0, 0]))
                        glEnd()
                elif Toggle_bvhRenderingMode == BoxRendering:
                    if self.parent:
                        y = np.array([0., 1., 0.])
                        cos = np.dot(y, self.offset) / (np.sqrt(np.dot(self.offset, self.offset)) * np.sqrt(np.dot(y, y)))
                        cross = np.cross(y, self.offset)
                        glPushMatrix()
                        glRotatef(np.degrees(np.arccos(cos)), cross[0], cross[1], cross[2])
                        glScalef(.05, np.sqrt(self.offset @ self.offset), .05)
                        # glScalef(50, 1, 50)
                        drawUnitCube_glDrawArray()
                        glPopMatrix()
            child.drawJoint()
        glPopMatrix()
        
    def animateJoint(self, frame):
        global Toggle_bvhRenderingMode, BoxRendering, LineRendering, motion
        glPushMatrix()
        glTranslatef(self.offset[0], self.offset[1], self.offset[2])
        glColor3ub(150, 150, 255)
        if Toggle_bvhRenderingMode == LineRendering:
            if self.parent:
                glBegin(GL_LINES)
                glColor3ub(150, 150, 255)
                glVertex3fv(-self.offset)
                glVertex3fv(np.array([0, 0, 0]))
                glEnd()
        elif Toggle_bvhRenderingMode == BoxRendering:
            if self.parent:
                y = np.array([0., 1., 0.])
                cos = np.dot(y, self.offset) / (np.sqrt(np.dot(self.offset, self.offset)) * np.sqrt(np.dot(y, y)))
                cross = np.cross(y, self.offset)
                glPushMatrix()
                glRotatef(np.degrees(np.arccos(cos)), cross[0], cross[1], cross[2])
                glScalef(.05, np.sqrt(self.offset @ self.offset), .05)
                # glScalef(50, 1, 50)
                drawUnitCube_glDrawArray()
                glPopMatrix()
        i = 0
        for i, chan in zip(self.motionidx, self.channel):
            if chan.upper() == 'XROTATION':
                glRotatef(motions[frame][i], 1, 0, 0)
            elif chan.upper() == 'YROTATION':
                glRotatef(motions[frame][i], 0, 1, 0)
            elif chan.upper() == 'ZROTATION':
                glRotatef(motions[frame][i], 0, 0, 1)
            elif chan.upper() == 'XPOSITION':
                glTranslatef(motions[frame][i], 0, 0)
            elif chan.upper() == 'YPOSITION':
                glTranslatef(0, motions[frame][i], 0)
            elif chan.upper() == 'ZPOSITION':
                glTranslatef(0, 0, motions[frame][i])
        for child in self.child:
            child.animateJoint(frame)
        glPopMatrix()

def drawObj(offset, varr):
    y = np.array([0., 1., 0.])
    cos = np.dot(y, offset) / (np.sqrt(np.dot(offset, offset))
                               * np.sqrt(np.dot(y, y)))
    cross = np.cross(y, offset)
    varr = np.array(varr)

    glPushMatrix()
    glRotatef(np.degrees(np.arccos(cos)), cross[0], cross[1], cross[2])
    glScalef(.1, .1, .1)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize,
                    ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

    glPopMatrix()

def bvhRender(paths):
    global bvh, isbvhcreated, isObj, motions
    name = paths.split('/')[-1]
    bvh = Bvh(name)
    motions.clear()
    isbvhcreated = True
    bvh.parsebvhFile(paths)
    bvh.printInfo()
    # if name == 'sample-walk.bvh':
    #     isObj = True
    #     bvh.setArr()


def parseOBJ(paths):
    vertex = []
    normal = []
    pairs = []

    f = open(paths)

    while True:
        line = f.readline()
        if not line:
            break

        words= line.split()

        if words[0] == 'v':
            vertex.append(np.array((float(words[1]), float(words[2]), float(words[3]))))
        elif words[0] == 'vn':
            normal.append((float(words[1]), float(words[2]), float(words[3])))
        elif words[0] == 'f':
            pair = []
            tmp = []
            for i in range(1, len(words)):
                v, t, n = words[i].split('/')
                pair.append((int(n)-1, int(v)-1))
            pairs.append(np.array(pair))

    varr = makeVarr(normal, vertex, pairs)

    return np.array(varr, 'float32')


def makeVarr(normal, vertex, pairs):
    varr = []
    for pair in pairs:
        for i in range(1, len(pair)-1):
            varr.append(normal[pair[0, 0]])
            varr.append(vertex[pair[0, 1]])
            varr.append(normal[pair[i, 0]])
            varr.append(vertex[pair[i, 1]])
            varr.append(normal[pair[i+1, 0]])
            varr.append(vertex[pair[i+1, 1]])
    return varr


def normalize(v):
    return np.array(v) / np.sqrt(v @ v)


def render():
    global ArimuthAngle, ElevationAngle, u, v, w, EyePoint, TargetPoint, UpVector, varr, fvarr, snarr, fnarr, iarr
    global Toggle_Polygon, Toggle_Projection, Toggle_RenderingMode, bvh, bvhAnimate, isbvhcreated
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

    glDisable(GL_LIGHTING)
    if isbvhcreated:
        if bvhAnimate:
            bvh.animatebvh()
        else:
            bvh.drawbvh()


def main():
    global varr, fvarr, snarr, fnarr, iarr, gVertexArraySeparate

    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "bvh Viewer", None, None)

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

    gVertexArraySeparate = createVertexArraySeparate()
    # Initialize Vectors for Object File Render
    varr = np.empty((0, 3))
    fvarr = np.empty((0, 3))
    fnarr = np.empty((0, 3))
    iarr = np.empty((0, 3), np.int32)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
