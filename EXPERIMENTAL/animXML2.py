import xml.etree.ElementTree as ET
import animWrite as AW
from mathutils import *
import children as CH



fileName = "models/" + "daenamehere.dae"

tree = ET.parse(fileName)
root = tree.getroot()
parent_map = dict((c, p) for p in tree.iter() for c in p)
fullNodeArray = []
armatureName = ''

visualScene = root.find('{http://www.collada.org/2005/11/COLLADASchema}library_visual_scenes')

FirstBone = visualScene[0][0]


def main():
    def getAllChildren(startPoint, parentMap, armName):
        for o in startPoint:
            if o.get('type') == 'JOINT':
                # print(o.get("sid"))

                loc, rot, scale = CH.decomposeMatrix(o[0].text)

                allFrames = CH.getFrames(o.get('sid'), armName)
                classic = ''
                if parentMap[o].get('type') == 'NODE':
                    classic = parentMap[o].get('name')
                else:
                    classic = parentMap[o].get('sid')

                halfArray = [o.get("sid"), classic, allFrames]
                fullNodeArray.append(halfArray)
                getAllChildren(o, parentMap, armName)

            else:

                continue

    if FirstBone.get('type') == 'NODE':
        armatureName = FirstBone.get('name')
        loc, rot, scale = CH.decomposeMatrix(FirstBone[0].text)

        tempArray = [FirstBone.get('name'), "", [
            [int(float(rot[1]) * 32512), int(float(rot[2]) * 32512), int(float(rot[3]) * 32512),
             int(float(rot[0]) * 32512),
             loc[0], loc[1], loc[2], scale[0], scale[1], scale[2]]]]  # Use now

        # [parent, child, [all frames in here as xyzw xyz ]]
        # print(armatureName)
        # QUAT POS SCA

        fullNodeArray.append(tempArray)
        getAllChildren(FirstBone, parent_map, armatureName)

    print(fullNodeArray)
    AW.head()
    AW.node2(fullNodeArray)
    AW.wend()


if __name__ == "__main__":
    main()
