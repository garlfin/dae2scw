import numpy as np
from transformations import *
import xml.etree.ElementTree as ET
from squaternion import euler2quat, quat2euler, Quaternion
import animWrite as AW
import index
from mathutils import *

# scale, shear, angles, trans, persp = decompose_matrix(matrix)

# [name,parent,[rot,pos,scale array]]
tree = ET.parse("models/tvcute.dae")
root = tree.getroot()
parent_map = dict((c, p) for p in tree.iter() for c in p)
fullNodeArray = []
armName = ''
def getAllChildren(startPoint):
    for o in startPoint:
        if o.get('type') == 'JOINT':
            #print('here')
            library_animations = root.findall('{http://www.collada.org/2005/11/COLLADASchema}library_animations')[0][0]
            for g in library_animations:
                wholeArmAction = armName+'_'+armName+'Action_'+o.get('sid')+'_pose_matrix'
                #print(o.get('sid'))
                #print(wholeArmAction)
                #print(g.get('id'))
                if g.get('id') == wholeArmAction:
                    print(g.get('id'))
                    transformMatrix = list(map(float, g[1][0].text.split()))
                    composite_list = [transformMatrix[x:x + 16] for x in range(0, len(transformMatrix), 16)]
                    if parent_map[o].get('type') == 'NODE':
                        classic = parent_map[o].get('name')
                    else:
                        classic = parent_map[o].get('sid')
                    tempArray = [o.get('sid'), classic]
                    allAnimTemp = []
                    tempTrans = []
                    for y in composite_list:
                        matrx = [y[i:i+4] for i in range(0,16,4)]
                        print(matrx)
                        #print(rot)
                        trans, rot, scale = Matrix(matrx).decompose()
                        print(rot)
                        #xyz = rot.to_euler()
                        #xyzconv = [xyz[0],xyz[1],xyz[2]]
                        #rot = Euler(xyzconv).to_quaternion()
                        #
                        #q = euler2quat(angles[0], angles[1], angles[2], degrees=False)
                        #print(rot,' ?')

                        #print(q)
                        # print(q[1], ' ', q[2], ' ', q[3], ' ', q[0], ' rot')
                        tempTrans= [int(float(rot[1])*32512),int(float(rot[2])*32512),int(float(rot[3])*32512),int(float(rot[0])*32512),trans[0],trans[1],trans[2],scale[0],scale[1],scale[2]]
                        allAnimTemp.append(tempTrans)
                    tempArray.append(allAnimTemp)
                    fullNodeArray.append(tempArray)




            #q = euler2quat(rotz, roty, rotx, degrees=True)


            #print(scale)
            #rint(parent_map[o].get('sid'))
            if parent_map[o].get('type') == 'NODE':
                classic = parent_map[o].get('name')
            else:
                classic = parent_map[o].get('sid')

            #tempArray = [o.get('sid'), classic, allTransformsArray ]
            #fullNodeArray.append(tempArray)

            getAllChildren(o)


for cont in root.findall('{http://www.collada.org/2005/11/COLLADASchema}library_visual_scenes'):
    FirstBone = cont[0][0]
    if FirstBone.get('type') == 'NODE':



        # print(rotx,' ',roty,' ',rotz)

        # q = euler2quat(rotz, roty, rotx, degrees=True)
        armName = FirstBone.get('name')
        #tempArray = [FirstBone.get('name'), "",[[ 0,0,32512,0, 0, 0, 0, 1, 1, 1]]] # Use this after testing
        tempArray = [FirstBone.get('name'), "", [[0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]] # Use now
        # ROT X Y Z #POS X Y Z #SCALE X Y Z
        fullNodeArray.append(tempArray)
        getAllChildren(FirstBone)
AW.head()
AW.node2(fullNodeArray)
AW.wend()
