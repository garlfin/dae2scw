import index
import xml.etree.ElementTree as ET
import numpy as np
from squaternion import *
f = open("demofile2.txt", "a")
f.truncate(0)

tree = ET.parse("models/tvcute.dae")
root = tree.getroot()
# print(root)
index.head()
Allname = []
for country in root.findall('{http://www.collada.org/2005/11/COLLADASchema}library_geometries'):
    for child in country:
        print('skin[source="#%s"]' % child.get('id'))
        # {http://www.collada.org/2005/11/COLLADASchema}

        for cont in root.findall('{http://www.collada.org/2005/11/COLLADASchema}library_controllers'):
            for contchild in cont:
                for contchildchild in contchild:
                    if contchildchild.get('source') == '#%s' % child.get('id'):
                        bind = list(map(float, contchildchild[0].text.split()))
                        jointnames = list(contchildchild[1][0].text.split())
                        jointvalues = list(map(float, contchildchild[2][0].text.split()))
                        weightsdata = list(map(float, contchildchild[3][0].text.split()))
                        vcount = list(map(float, contchildchild[5][2].text.split()))
                        weightsinfo = list(map(float, contchildchild[5][3].text.split()))
                        i = 0
                        allvalues = []
                        for l in vcount:
                            if l == 1:
                                # allvalues += weightsinfo[i*2]

                                allvalues.append([int(weightsinfo[0]), 0, 0, 0,
                                                  int(weightsdata[int(weightsinfo[1])] * 65535), 0, 0, 0])
                                del(weightsinfo[0])
                                del (weightsinfo[0])
                            elif l == 2:
                                allvalues.append([int(weightsinfo[0]),int(weightsinfo[2]),0,0,int(weightsdata[int(weightsinfo[1])] * 65535),int(weightsdata[int(weightsinfo[3])] * 65535),0,0])
                                del(weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])

                            elif l == 3:

                                allvalues.append([int(weightsinfo[0]), int(weightsinfo[2]), int(weightsinfo[4]), 0,
                                                 int(weightsdata[int(weightsinfo[1])] * 65535),
                                                 int(weightsdata[int(weightsinfo[3])] * 65535), int(weightsdata[int(weightsinfo[5])] * 65535), 0])

                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])

                            elif l == 4:
                                allvalues.append([int(weightsinfo[0]), int(weightsinfo[2]), int(weightsinfo[4]), int(weightsinfo[6]),
                                                 int(weightsdata[int(weightsinfo[1])] * 65535),
                                                 int(weightsdata[int(weightsinfo[3])] * 65535),
                                                 int(weightsdata[int(weightsinfo[5])] * 65535), int(weightsdata[int(weightsinfo[7])] * 65535)])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])
                                del (weightsinfo[0])


                        # f.write(str(allvalues))
                        # print(contchildchild[2][0].text)
                        # print(contchildchild[0].text)
                        composite_list = [jointvalues[x:x + 16] for x in range(0, len(jointvalues), 16)]
                        # print(composite_list)

                        print(composite_list)

                        # f.write()

        print()
        print(child[0][0].get('id'))

        v = list(map(float, child[0][0][0].text.split()))
        print(v)
        print(child[0][1].get('id'))

        vn = list(map(float, child[0][1][0].text.split()))
        print(vn)
        print(child[0][2].get('id'))

        vt = list(map(float, child[0][2][0].text.split()))
        vt[1::2] = [x * -1 + 1 for x in vt[1::2]]
        print(vt)
        print(child.get('id') + '-triangles-0')

        tri = list(map(float, child[0][4][3].text.split()))
        print(tri)
        name = child.get('id')
        Allname.append(name)

        index.geom(name, v, vn, vt, tri, bind, jointnames, jointvalues, allvalues)

tempArray = []
fullNodeArray = []
parent_map = dict((c, p) for p in tree.iter() for c in p)




def getAllChildren(startPoint):
    for o in startPoint:
        if o.get('type') == 'JOINT':
            scale = list(map(float, o[0].text.split()))
            pos = list(map(float, o[4].text.split()))
            rot1 = list(map(float, o[1].text.split()))
            rot2 = list(map(float, o[2].text.split()))
            rot3 = list(map(float, o[3].text.split()))

            rotx = rot3[3]
            roty = rot2[3]
            rotz = rot1[3]
            #print(rotx,' ',roty,' ',rotz)

            q = euler2quat(rotz, roty, rotx, degrees=True)
            print(q[1],' ', q[2], ' ', q[3], ' ',q[0], ' ', pos[0])

            #print(scale)
            #rint(parent_map[o].get('sid'))
            if parent_map[o].get('type') == 'NODE':
                classic = parent_map[o].get('name')
            else:
                classic = parent_map[o].get('sid')
            tempArray = [o.get('sid'), classic, q[1], q[2], q[3], q[0], pos[0], pos[1], pos[2], scale[0],
                         scale[1], scale[2]]
            fullNodeArray.append(tempArray)
            getAllChildren(o)


for cont in root.findall('{http://www.collada.org/2005/11/COLLADASchema}library_visual_scenes'):
    FirstBone = cont[0][0]
    if FirstBone.get('type') == 'NODE':

        rot1 = list(map(float, FirstBone[1].text.split()))
        rot2 = list(map(float, FirstBone[2].text.split()))
        rot3 = list(map(float, FirstBone[3].text.split()))

        rotx = rot3[3]
        roty = rot2[3]
        rotz = rot1[3]
        # print(rotx,' ',roty,' ',rotz)

        q = euler2quat(rotz, roty, rotx, degrees=True)
        tempArray = [FirstBone.get('name'), "", q[1], q[2], q[3], q[0], 0, 0, 0, 1, 1, 1]
        # ROT X Y Z #POS X Y Z #SCALE X Y Z
        fullNodeArray.append(tempArray)
        getAllChildren(FirstBone)

# f.write(g.get('name')," || ",g.find('..').get('name'))
#print(fullNodeArray)
index.node2(Allname, fullNodeArray)
index.wend()
f.close()
