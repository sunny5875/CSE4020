import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


zoom = 5
xPos = 0
yPos = 0

oldxPos = 0
oldyPos = 0

right = False
left = False
isPerspective= True

gElevation = np.radians(36.264)
gAzimuth = np.radians(45.)
upVector = np.array([0.,1.,0.])

center = np.array([0.,0.,0.])

global gVertexArrayIndexed, gIndexArray
global M,u,v,w
global path,anim
isDrag = False

global varr,iarr,narr,smoothNarr,varr_
global earthNarr,earthVarr,moonNarr,moonVarr,sunNarr,sunVarr,backGroundNarr,backGroundVarr
global earthSmoothNarr,earthVarr_,moonVarr_,moonSmoothNarr,sunVarr_,sunSmoothNarr,backGroundVarr_,backGroundSmoothNarr,earthIarr,moonIarr,sunIarr,backgroundIarr

isHierarchicalMode = False
iswireframeMode = True
isSmoothShading = False
isFirst = True
isAnimate = False
isBox = True
motion = []

               
# draw coordinate
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
    

global glVertexArrayIndexed,glIndexArray

def createVertexArraySeparate():
    varr = np.array([
            (-0.5773502691896258,0.5773502691896258,0.5773502691896258),         # v0 normal
            ( -0.02 ,  0 ,  0.02 ), # v0 position
            (0.8164965809277261,0.4082482904638631,0.4082482904638631),         # v2 normal
            (  0.02 , 0 ,  0.02 ), # v2 position
            (0.4082482904638631,-0.4082482904638631,0.8164965809277261),         # v1 normal
            (  0.02 ,  -1 ,  0.02 ), # v1 position

            (-0.4082482904638631,-0.8164965809277261,0.4082482904638631),         # v0 normal
            ( -0.02 ,  -1 ,  0.02 ), # v0 position
            (-0.4082482904638631,0.4082482904638631,-0.8164965809277261),         # v3 normal
            ( -0.02 , 0 ,  -0.02 ), # v3 position
            (0.4082482904638631,0.8164965809277261,-0.4082482904638631),         # v2 normal
            (  0.02 , 0 ,  -0.02 ), # v2 position

            (0.5773502691896258,-0.5773502691896258,-0.5773502691896258),
            ( 0.02 ,  -1 , -0.02 ), # v4
            (-0.8164965809277261,-0.4082482904638631,-0.4082482904638631),
            (  -0.02 ,  -1 , -0.02 ), # v5
          
            ], 'float32')

            
    iarr = np.array([
    (0,2,1),
    (0,3,2),
    (4,5,6),
    (4,6,7),
    (0,1,5),
    (0,5,4),
    (3,6,2),
    (3,7,6),
    (1,2,6),
    (1,6,5),
    (0,7,3),
    (0,4,7)
    ], dtype = 'int32')
    return varr,iarr

def drawCube_glDrawElements():

    glVertexArrayIndexed,glIndexArray = createVertexArraySeparate()

    varr = glVertexArrayIndexed
    iarr = glIndexArray
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    glNormalPointer(GL_FLOAT,6*iarr.itemsize,varr)
    glVertexPointer(3,GL_FLOAT,6*iarr.itemsize,ctypes.c_void_p(varr.ctypes.data+3*iarr.itemsize))
    glDrawElements(GL_TRIANGLES,iarr.size,GL_UNSIGNED_INT,iarr)
    
    

            

    
# grid varr, iarr
def createVertexAndIndexArrayIndexed():
    varr = np.array([
            (-5,0,5),(-4,0,5),(-3,0,5),(-2,0,5),(-1,0,5),(0,0,5),(1,0,5),
            (2,0,5),(3,0,5),(4,0,5),(5,0,5),(5,0,4),(5,0,3),(5,0,2),
            (5,0,1),(5,0,0),(5,0,-1),(5,0,-2),(5,0,-3),(5,0,-4),(5,0,-5),
                
            (4,0,-5),(3,0,-5),(2,0,-5),(1,0,-5),(0,0,-5),(-1,0,-5),(-2,0,-5),
            (-3,0,-5),(-4,0,-5),(-5,0,-5),(-5,0,-4),(-5,0,-3),(-5,0,-2),(-5,0,-1),
            (-5,0,0),(-5,0,1),(-5,0,2),(-5,0,3),(-5,0,4)
            
            ], 'float32')
    iarr = np.array([(0,10),(20,30),
            (0,30),(1,29),(2,28),(3,27),(4,26),(5,25),(6,24),(7,23),(8,22),(9,21),(10,20),
            (11,39),(12,38),(13,37),(14,36),(15,35),(16,34),(17,33),(18,32),(19,31),(20,30)
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
    global zoom,center,gAzimuth,gElevation,upVector,M,u,v,w
    
#   calculate camera's coordinate system
    w = np.array([np.cos(gElevation) * np.sin(gAzimuth), np.sin(gElevation),np.cos(gElevation)*np.cos(gAzimuth)])

    w=w/np.sqrt(np.dot(w,w))

    u = np.cross(upVector,w)
    u = u / np.sqrt(np.dot(u,u))

    v = np.cross(w,u)
    v = v / np.sqrt(np.dot(v,v))

#   get viewing transformation
    M = np.identity(4)
    M[:3,0]=u
    M[:3,1]=v
    M[:3,2]=w
    M[:3,3]=w*zoom + center

    M = np.linalg.inv(M)

#hierarchical model
def drawHierarchicalModel() :
    global earthNarr,earthVarr,moonNarr,moonVarr,sunNarr,sunVarr,backGroundVarr,backGroundNarr,earthSmoothNarr,earthVarr_,moonVarr_,moonSmoothNarr,sunVarr_,sunSmoothNarr,backGroundVarr_,backGroundSmoothNarr,earthIarr,moonIarr,sunIarr,backgroundIarr
    t = glfw.get_time()
   
#   background
    glPushMatrix()
    glTranslatef(0.8,2.3,0.3)
    glScalef(0.03,0.03,0.03)
    drawObject(backGroundNarr,backGroundVarr,backGroundSmoothNarr,backGroundVarr_,backgroundIarr)
    glScalef(-1,-1,1)
    glTranslatef(100,200,50)
    drawObject(backGroundNarr,backGroundVarr,backGroundSmoothNarr,backGroundVarr_,backgroundIarr)
    glPopMatrix()
    
#    sun
    glPushMatrix()
    glScalef(1+np.abs(np.sin(t)/10.0),1+np.abs(np.sin(t)/10.0),1+np.abs(np.sin(t)/10.0))
    glRotatef(t*(180/np.pi),0,1,0)
    
    glPushMatrix()
    glScalef(0.009,0.009,0.009)
    
    glPushMatrix()
    glScalef(100,100,100)
    glPushMatrix()
    drawObject(sunNarr,sunVarr,sunSmoothNarr,sunVarr_,sunIarr)
    glPopMatrix()
    glPopMatrix()

#    earth
    glPushMatrix()
    glRotatef(t*(180/np.pi),0,1,0)
    glPushMatrix()
    glTranslate(100,100,40)
    glScalef(10,10,10)
    glPushMatrix()
    glRotatef(t*(180/np.pi),0,1,0)
    drawObject(earthNarr,earthVarr,earthSmoothNarr,earthVarr_,earthIarr)
    glPopMatrix()

#   moon
    glPushMatrix()
    glRotatef(2*t*(180/np.pi),0,1,0)

    glPushMatrix()
    glTranslate(2,0,2)
    glScalef(.007,.007,.007)
#    glScalef(1000,1000,1000)
    glRotatef(2*t*(180/np.pi),0,1,0)
    drawObject(moonNarr,moonVarr,moonSmoothNarr,moonVarr_,moonIarr)

    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    


def render():
    global isPerspective,M,zoom,center,gAzimuth,gElevation,upVector,isDrag,iswireframeMode,isHierarchicalMode,narr,varr,smoothNarr,varr_,anim,isAnimate
        
#    wireframe mode
    if (iswireframeMode == True):
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
  

#  check perspective /ortho
    if(isPerspective == True):
        gluPerspective(45, 1, 1,10)
    else :
        glOrtho (-2.5,2.5,-2.5,2.5,-10,10)
    
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
    lightPos = (1.,2.,1.,1.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    # light intensity for each color channel
    lightColor = (1.,1,0,1.)
    ambientLightColor = (.1,.0,.0,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    
    glPushMatrix()
    
#    light color2
    lightPos = (-3.,-2.,1.,1.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()

    # light intensity for each color channel
    lightColor = (0.,1.,1.,1.)
    ambientLightColor = (.0,.1,0.,1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

#    glPushMatrix()
#
##    light color3
#    lightPos = (3.,-5.,3.,1.)    # try to change 4th element to 0. or 1.
#    glLightfv(GL_LIGHT3, GL_POSITION, lightPos)
#    glPopMatrix()
#
#    # light intensity for each color channel
#    lightColor = (0.,0.,1.,1.)
#    ambientLightColor = (.0,.0,.1,1.)
#    glLightfv(GL_LIGHT3, GL_DIFFUSE, lightColor)
#    glLightfv(GL_LIGHT3, GL_SPECULAR, lightColor)
#    glLightfv(GL_LIGHT3, GL_AMBIENT, ambientLightColor)



    # material reflectance for each color channel
    objectColor = (1,1,1,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
   

    if(isBox == False):
         glDisable(GL_LIGHTING)

    if(isDrag == True and isHierarchicalMode == False and isAnimate == False):
#        drawObject(narr,varr,smoothNarr,varr_,iarr)
        anim.drawSkeleton()
    
    if(isAnimate == True):
        anim.animateMotion()
    
    
    
    if(isHierarchicalMode == True):
        drawHierarchicalModel()
    

    



   
# make vector's size 1
def normalized(v):
    l = np.sqrt(np.dot(v,v))
    return 1/l * np.array(v)


    

# obj parser and calculate varr,narr,smoothNarr,varr_,iarr
def ObjRendering():
    global varr,iarr,file,narr,path,isFirst,isDrag,isSmoothShading,smoothNarr,varr_
#    drag and drop file
    if(isDrag == True):
        file = open(str(path)[2:-2],'r')
    else : #hierarchical mode file
        file = open(path,'r')
   
    
#    initialize
    varr = np.empty((0,3),float)
    iarr = np.empty((0,3), np.int32)
    narr = np.empty((0,3),float)
    narr_ = np.empty((0,3),float)
    varr_ = np.empty((0,3), float)

    

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

        
        line = line.replace("\n","")
        splitLine = line.split()
        line=line[2:]
     
#        f parsing
        if splitLine[0] == 'f':
            if(len(splitLine) == 4):
                face3Count += 1
            elif(len(splitLine) == 5):
                face4Count += 1
            else :
                faceMoreThan4Count += 1
                    
            
            index = np.empty((0,3),np.int32)
            item = np.empty((0,3),np.float32)
            
            for word in splitLine:
                if(word == splitLine[0]):
                    continue
                                                    
                v = word.split('/')
                
                index = np.append(index, (int(v[0])-1))
        
                
                if len(v) == 3:
                    item = np.append(item,[narr_[int(v[2])-1]],axis=0)
            
                
#    triangluration
            if(len(index) != 3):
                index1 = np.array([index[0],index[1],index[2]])
                index2 = np.array([index[0],index[2],index[3]])
                for i in range(2, len(index)):
                    temp_index = np.array([index[0],index[i-1],index[i]])
                    iarr = np.append(iarr, np.array([temp_index]), axis=0)
                    
                    temp_item = np.array([np.array(item[0]),np.array(item[i-1]),np.array(item[i])])
                    narr = np.append(narr,temp_item,axis=0)
            else :
                iarr = np.append(iarr,np.array([index]),axis=0)
                for i in item:
                    narr = np.append(narr,np.array([i]),axis=0)
               
        
#   vn parsing
        elif splitLine[0] == 'vn':
            item= normalized([float(splitLine[1]),float(splitLine[2]),float(splitLine[3])])
            narr_ = np.append(narr_, np.array([item]),axis=0)

#    v parsing
        elif splitLine[0] =='v':
            
            item = np.array([[float(splitLine[1]),float(splitLine[2]),float(splitLine[3])]])
            varr_ = np.append(varr_,item,axis=0)
            

#    normalCountArr = np.zeros((len(varr_),),float)
    smoothNarr = np.zeros((len(varr_),3),float)
  
    
    j = 0
    for index in iarr:
        for item in index:
#            normalCountArr[item] += 1
            varr = np.append(varr,np.array([varr_[item]]),axis=0)
            smoothNarr[item] += narr[j]
            j+=1
            


#   calculate smoothNarr
    for i in range(len(varr_)):
#        smoothNarr[i] /= np.full((3,),float(normalCountArr[i]))
        smoothNarr[i]=normalized(smoothNarr[i])
         
    


    if isFirst == False :
        print("file name : "+ str(path[0]))
        print("total number of faces : " + str(len(iarr)))
        print("number of faces with 3 vertices : " + str(face3Count))
        print("number of faces with 4 vertices : " + str(face4Count))
        print("number of faces with  more than 4 vertices : " + str(faceMoreThan4Count))
    
   
    varr= varr.astype(np.float32)
#    iarr= varr.astype(np.int32)
    narr = narr.astype(np.float32)
    varr_ = varr_.astype(np.float32)
    smoothNarr = smoothNarr.astype(np.float32)
    
 
    
    return narr,varr,smoothNarr,varr_,iarr

class BvhJoint:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.offset = np.zeros(3)
        self.channelOrder = []
        self.channelIdx = []
        self.children = []
        self.rotationMatrix = list()
        self.position = list()
        self.channels = list()
        

    def addChild(self, child):
        self.children.append(child)

    def draw(self):
        global isBox
        
        glPushMatrix()
        #parent 기준으로 떨어진 위치
        glTranslatef(self.offset[0], self.offset[1], self.offset[2])

        
        if(isBox == True):
            if self.parent:
                offset = np.sqrt(self.offset[0]**2+self.offset[1]**2+self.offset[2]**2)
                
                
                degree = np.cross(normalized(self.offset),np.array([0,1,0]))
                degreeSize = np.rad2deg(np.arcsin(np.sqrt(degree[0]**2+degree[1]**2+degree[2]**2)))
                if np.dot(self.offset, np.array([0,1,0])) > 0:
                    degreeSize = 180 - degreeSize
                glPushMatrix()
                glRotatef(degreeSize,degree[0],degree[1],degree[2])
                
                glScalef(1,-offset, 1)
                drawCube_glDrawElements()
                glPopMatrix()
        else :
            if self.parent:
                glBegin(GL_LINES)
                #parent의 위치 : offset의 음수값
                glVertex3fv(-self.offset)
                #현재 joint의 위치 : 이미 이동했으므로 원점
                glVertex3fv(np.array([0.,0.,0.]))
                glEnd()
        

        for child in self.children:
            child.draw()
        glPopMatrix()

    def animate(self, frameNumber):
        global motion, isBox
        
        
        glPushMatrix()
        glTranslatef(self.offset[0], self.offset[1], self.offset[2])
        
        if(isBox == True):
            if self.parent:
                offset = np.sqrt(self.offset[0]**2+self.offset[1]**2+self.offset[2]**2)
                
                
                degree = np.cross(normalized(self.offset),np.array([0,1,0]))
                degreeSize = np.rad2deg(np.arcsin(np.sqrt(degree[0]**2+degree[1]**2+degree[2]**2)))
                if np.dot(self.offset, np.array([0,1,0])) > 0:
                    degreeSize = 180 - degreeSize
                glPushMatrix()
                glRotatef(degreeSize,degree[0],degree[1],degree[2])
                
                glScalef(1,-offset, 1)
                drawCube_glDrawElements()
                glPopMatrix()
        else :
            if self.parent:
                glBegin(GL_LINES)
                #parent의 위치 : offset의 음수값
                glVertex3fv(-self.offset)
                #현재 joint의 위치 : 이미 이동했으므로 원점
                glVertex3fv(np.array([0.,0.,0.]))
                glEnd()
                
        # 지금 joint를 기준으로 한 움직임 계산
        # channelIdx는 한 프레임의 움직임 값 중 현재 joint에 해당하는 인덱스
        # channelOrder는 움직임의 유형
        for motion_idx, motion_type in zip(self.channelIdx, self.channelOrder):
            if motion_type.lower() == 'xrotation':
                glRotatef(motion[frameNumber][motion_idx], 1, 0, 0)
            elif motion_type.lower() == 'yrotation':
                glRotatef(motion[frameNumber][motion_idx], 0, 1, 0)
            elif motion_type.lower() == 'zrotation':
                glRotatef(motion[frameNumber][motion_idx], 0, 0, 1)
            
            elif motion_type.lower() == 'xposition':
                glTranslatef(motion[frameNumber][motion_idx], 0, 0)
            elif motion_type.lower() == 'yposition':
                glTranslatef(0, motion[frameNumber][motion_idx], 0)
            elif motion_type.lower() == 'zposition':
                glTranslatef(0, 0, motion[frameNumber][motion_idx])
            
        for child in self.children:
            child.animate(frameNumber)
        glPopMatrix()

class Bvh:
    def __init__(self):
        self.joints = {} #dictionary of joints
        self.root = None #root joints
        self.frames = 0 #number of frame
        self.fps = 0 #fps
      

    def parseFile(self, path):
        with open(path, 'r') as f:
            self.divideHierarchyAndMotion(f.read())
            
    def parseHierarchy(self, text):
    
        lines = text.split("\n")
       

        jointStack = []
        cidx = 0
        for line in lines:

            line =line.strip()
            words = line.split(" ")
          
            instruction = words[0]

            if instruction.upper() == "JOINT" or instruction.upper() == "ROOT":
                parent = jointStack[-1] if instruction.upper() == "JOINT" else None
                joint = BvhJoint(words[1], parent)
            
                self.joints[joint.name] = joint
               
                if parent:
                    parent.addChild(joint)
               
                jointStack.append(joint)
                
                if instruction.upper() == "ROOT":
                    self.root = joint
                    
            elif instruction.upper() == "CHANNELS":
                for i in range(2, len(words)):
                    jointStack[-1].channelIdx.append(cidx)
                    cidx+=1
                    jointStack[-1].channelOrder.append(words[i])
               
            elif instruction.upper() == "OFFSET":
                for i in range(1, len(words)):
                    jointStack[-1].offset[i - 1] = float(words[i])
                    
            elif instruction == "End":
                joint = BvhJoint(jointStack[-1].name + "_end", jointStack[-1])
                jointStack[-1].addChild(joint)
                jointStack.append(joint)
                self.joints[joint.name] = joint
                       
            elif instruction == '}':
                jointStack.pop()

   

    def parseMotion(self, text):
        global  motion
        motion.clear()
    
        
        lines = text.split("\n")

  
        for line in lines:
            if line == '':
                continue

            line = line.replace("\n", "")
            line = line.strip()
            line = line.replace("\t"," ")
           
            
            if line.startswith("Frame Time: "):
                self.fps = round(1 / float(line.split(" ")[2]))
                continue
            if line.startswith("Frames:"):
                
                self.frames = int(line.split(" ")[1])
            
                continue
            
            line = line.split()
            line = list(map(float, line))
            motion.append(line)
           






    def divideHierarchyAndMotion(self, text):
        hierarchy, motion = text.split("MOTION")
        self.parseHierarchy(hierarchy)
        self.parseMotion(motion)

    def drawSkeleton(self):
        
        glPushMatrix()
        # 다운로드한 파일의 경우 scale
#        glScalef(.01,.01,.01)
        self.root.draw()
        glPopMatrix()
        
    def animateMotion(self):
        global pressTime,anim,positionMatrixf
        time = glfw.get_time()-pressTime
        frameNumber = int(time* (self.fps))% self.frames
        
        glPushMatrix()
        # 다운로드한 파일의 경우 scale
#        glScalef(.01,.01,.01)
        self.root.animate(frameNumber)
        glPopMatrix()
            

    def printBvhInformation(self):
        global path
        print("File name : " + str(path[0]))
        print("Number of frames :"+ str(self.frames)+" frames")
        print("FPS : "+str(self.fps))
        print("Number of joints : "+str(len(self.joints.keys()))+" joints")
        print("List of all joint names : ")
        for i in self.joints.keys():
            print("\t"+ i)

    
    
def BvhRendering():
    global path,anim
    anim = Bvh()
    anim.parseFile(path[0])
    anim.printBvhInformation()
    
    
    
    
    
    
def drawObject(narr,varr,smoothNarr,varr_,iarr):
    global isSmoothShading
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
            
#   force smooth shading
    if(isSmoothShading == True) :
        glNormalPointer(GL_FLOAT,3*smoothNarr.itemsize,smoothNarr)
        glVertexPointer(3,GL_FLOAT,3*varr_.itemsize,varr_)
        glDrawElements(GL_TRIANGLES,iarr.size,GL_UNSIGNED_INT,iarr)

#  flat shading
    else :
        glNormalPointer(GL_FLOAT,3*narr.itemsize,narr)
        glVertexPointer(3,GL_FLOAT,3*varr.itemsize,varr)
        glDrawArrays(GL_TRIANGLES,0,int(varr.size / 3))


        

def cursor_callback(window, xpos,ypos):
    global oldxPos,oldyPos,xPos,yPos,right,left,gAzimuth,gElevation,center,u,v
    
    oldxPos=xPos
    oldyPos=yPos
    
    xPos=xpos
    yPos=ypos
#    orbit
    if(left == True):
        gAzimuth+=np.radians(-xPos+oldxPos)
        gElevation+=np.radians(-yPos+oldyPos)
        
        if np.cos(gElevation) < 0:
            upVector = -1.
        else:
            upVector = 1.
#    panning
    if(right == True):
        center= center +((+oldxPos-xPos)* u + (-oldyPos+yPos)* v)*0.01
        
        
    
  

def mouse_button_callback(window, button, action, mods):
    global right,left
    if button == glfw.MOUSE_BUTTON_LEFT:
        if( action == glfw.PRESS):
                left = True
        elif action == glfw.RELEASE :
            left = False
    if button == glfw.MOUSE_BUTTON_RIGHT:
        if( action == glfw.PRESS):
                right = True
        elif action == glfw.RELEASE :
            right = False

    
#zooming
def scroll_callback(window, xoffset, yoffset):
    global zoom

    zoom+=yoffset*(-0.1)

#perspective & ortho
def key_callback(window,key,scancode, action, mods):
    global isPerspective,isHierarchicalMode,iswireframeMode,isSmoothShading,isAnimate,pressTime,isBox
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_V :
            isPerspective= not isPerspective
        if key == glfw.KEY_H:
            isHierarchicalMode = True
        if key == glfw.KEY_Z:
            iswireframeMode = not iswireframeMode
        if key == glfw.KEY_S:
            isSmoothShading = not isSmoothShading
        if key==glfw.KEY_SPACE:
            isAnimate = not isAnimate
            pressTime = glfw.get_time()
        if key == glfw.KEY_B :
            isBox = not isBox
           
    
            
#drag and drop
def fileparse(window,paths):
    global isDrag,isHierarchicalMode,path,isAnimate
    path= paths
#    ObjRendering()
    BvhRendering()
    isDrag = True
    isHierarchicalMode = False
    isAnimate = False

    
    
    
    


def main():
    global gVertexArrayIndexed, gIndexArray,path,earthNarr,earthVarr,moonNarr,moonVarr,sunNarr,sunVarr,isFirst,backGroundNarr,backGroundVarr,earthSmoothNarr,earthVarr_,moonVarr_,moonSmoothNarr,sunVarr_,sunSmoothNarr,backGroundVarr_,backGroundSmoothNarr,earthIarr,moonIarr,sunIarr,backgroundIarr,anim
    if not glfw.init():
        return
    window = glfw.create_window(700,700,'ClassAssignment3', None,None)
    if not window:
        glfw.terminate()
        return
        
    glfw.make_context_current(window)
    
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window,scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_key_callback(window,key_callback)
    glfw.set_drop_callback(window,fileparse)
    
    glfw.swap_interval(1)
   

    
    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
    myLookAt()
    
#    loading hiearichal mode
#    path = 'earth.obj'
#    earthNarr, earthVarr,earthSmoothNarr,earthVarr_,earthIarr =ObjRendering()
#
#    path = 'moon.obj'
#    moonNarr,moonVarr,moonSmoothNarr,moonVarr_,moonIarr = ObjRendering()
#
#    path = 'sun.obj'
#    sunNarr,sunVarr,sunSmoothNarr,sunVarr_,sunIarr =ObjRendering()
#
#    path = 'background.obj'
#    backGroundNarr,backGroundVarr,backGroundSmoothNarr,backGroundVarr_,backgroundIarr =ObjRendering()

    
    
    isFirst = False

    
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()
       
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
