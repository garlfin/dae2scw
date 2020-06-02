import xml.etree.ElementTree as ET
from mathutils import *
import animXML2 as aX2

print(aX2.fileName)
whatEver = aX2.fileName

tree = ET.parse(whatEver)
root = tree.getroot()
libraryAnimations = root.find('{http://www.collada.org/2005/11/COLLADASchema}library_animations')

def decomposeMatrix(rawMatrix):
    matrx = list(map(float, rawMatrix.split()))
    matrx2 = [matrx[i:i + 4] for i in range(0, 16, 4)]
    return Matrix(matrx2).decompose()


def getFrames(name, armatureName):
    actionContainer = "action_container-" + armatureName
    if libraryAnimations[0].get('id') == actionContainer:
        for x in libraryAnimations[0]:
            fullname = armatureName + "_" + armatureName + "Action_" + name + "_pose_matrix"
            if x.get("id") == fullname:
                transformMatrix = list(map(float, x[1][0].text.split()))
                composite_list = [transformMatrix[x:x + 16] for x in range(0, len(transformMatrix), 16)]
                allFramesArray = []
                for chunk in composite_list:
                    toDecompose = [chunk[i:i + 4] for i in range(0, 16, 4)]
                    trans, rot, scale = Matrix(toDecompose).decompose()
                    tempArray = [int(float(rot[1])*32512),int(float(rot[2])*32512),int(float(rot[3])*32512),int(float(rot[0])*32512),trans[0],trans[1],trans[2],scale[0],scale[1],scale[2]]
                    allFramesArray.append(tempArray)
                return allFramesArray
    else:
        for x in libraryAnimations:
            fullname = armatureName + "_" + name + "_pose_matrix"
            if x.get("id") == fullname:
                transformMatrix = list(map(float, x[1][0].text.split()))
                composite_list = [transformMatrix[x:x + 16] for x in range(0, len(transformMatrix), 16)]
                allFramesArray = []
                for chunk in composite_list:
                    toDecompose = [chunk[i:i + 4] for i in range(0, 16, 4)]
                    trans, rot, scale = Matrix(toDecompose).decompose()
                    tempArray = [int(float(rot[1])*32512),int(float(rot[2])*32512),int(float(rot[3])*32512),int(float(rot[0])*32512),trans[0],trans[1],trans[2],scale[0],scale[1],scale[2]]
                    allFramesArray.append(tempArray)
                return allFramesArray



