import struct
import binascii

# SC3D - 53 43 33 44
# Garlfin
# Why put > in struct.pack? > signifies big endian.



def fileDec(name):
    global path
    path = "scw/" + name[:-3] + "scw"
    global file
    file = open(path, "wb")
    
    print(path)

def head():
    headData = struct.pack('>4s', 'SC3D'.encode('utf-8'))
    # CHAR[4] MAGIC;
    headData2 = struct.pack('>I4shhhhH28sb', 39, 'HEAD'.encode('utf-8'), 2, 30, 0, 99, 28,
                            'sc3d/character_materials.scw'.encode('utf-8'), 0)
    # UINT ITEMSIZE; CHAR[4] ITEMTYPE; SHORT UNK; SHORT UNK1; SHORT UNK2; SHORT UNK3; USHORT STRINGLEN; CHAR[28] STRING; CHAR[0] REMAINING; UINT CRC;
    crc = binascii.crc32(headData2[4:])
    # CRC
    headData2 += struct.pack('>I', crc)
    # JOIN CRC TO MAIN STRUCT
    headData += headData2
    # JOIN STRUCTS
    file.write(headData)
    # WRITE TO FILE


def geom(name, v, vn, vt, tri,bindShapeMatrix,jointNames,jointValues,vertexWeights):
    toal = 0

    for y in jointNames:
        toal = toal + len(y)
    print(toal)
    print(int(len(jointNames) * 66)+toal)
    geomLen = 169 + len(name) + (len(v) / 3 * 6) + (len(vn) / 3 * 6) + (len(vt) / 2 * 4) + (len(tri) / 9 * 18) + int(len(jointNames)*66) + toal + int(len(v) / 3*12)
    print(geomLen)
    geomData = struct.pack('>I4sH', int(geomLen), 'GEOM'.encode('utf-8'), len(name))
    # UINT ITEMSIZE; CHAR[4] ITEMTYPE; USHORT STRINGLEN;
    for c in name:  # FOR EACH ITEM IN NAME, WRITE IT
        geomData += struct.pack('>c', bytes(c.encode('utf-8')))
    scalev = max(max(v), abs(min(v)))
    # Calculate scalev
    geomData += struct.pack('>H11sbH8sbHfI', 11, 'mainGeomGrp'.encode('utf-8'), 3, 8, 'POSITION'.encode('utf-8'), 0, 3,
                            scalev, int(len(v) / 3))
    # USHORT STRINGLEN; CHAR[1] STRING; CHAR VERTEXGROUPS; USHORT STRINGLEN; CHAR[8] STRING; CHAR INDEX; USHORT SHORTSV; FLOAT SCALEV; UINT VERTEXCOUNT;
    for x in v:
        geomData += struct.pack('>h', int(x * 32767 / scalev))
        # SHORT VERTEX;
        # Why x*32767/scalev? 32767 is the max size of an short(signed) and you gotta divide it by scalev to properly scale it(I guess)
    scalevn = max(max(vn), abs(min(vn)))
    geomData += struct.pack('>H6sbHfI', 6, 'NORMAL'.encode('utf-8'), 1, 3, scalevn, int(len(vn) / 3))
    # SHORT STRINGLEN; CHAR[6] STRING; CHAR INDEX; USHORT SHORTSVN; FLOAT SCALEVN; UINT VERTEXNORMCOUNT;
    for x in vn:
        geomData += struct.pack('>h', int(x * 32767 / scalevn))
        # SHORT VERTEXNORM;
        # Why x*32767/scalevn? 32767 is the max size of an short(signed) and you gotta divide it by scalevn to properly scale it(I guess)
    if max(max(vt), abs(min(vt))) <= 1:
        scalevt = 1
    else:
        scalevt = max(max(vt), abs(min(vt)))
    geomData += struct.pack('>H8sbHfI', 8, 'TEXCOORD'.encode('utf-8'), 2, 2, scalevt, int(len(vt) / 2))
    # SHORT STRINGLEN; CHAR[6] STRING; CHAR INDEX; USHORT SHORTSVT; FLOAT SCALEVT; UINT VERTEXTEXCOUNT;
    for x in vt:
        geomData += struct.pack('>h', int(x * 32767 / scalevt))
        # SHORT VERTEXNORM;
        # Why x*32767/scalevt? 32767 is the max size of an short(signed) and you gotta divide it by scalevt to properly scale it(I guess)
    geomData += struct.pack('>b', 1)
    # CHAR HASMATRIX;
    #bindShapeMatrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    for x in bindShapeMatrix:
        geomData += struct.pack('>f', x)



    # UNIMPLEMENTED #
    #geomData += struct.pack('>b', 0)
    geomData += struct.pack('>b', len(jointNames))
    # BYTE BONECOUNT;
    composite_list = [jointValues[x:x + 16] for x in range(0, len(jointValues), 16)]
    for x in range(0, len(composite_list)):
        print(jointNames[x])
        geomData+= struct.pack('>H',len(str(jointNames[x])))
        for s in jointNames[x]:
            geomData += struct.pack('>s',bytes(s.encode('utf-8')))
        for c in composite_list[x]:
            geomData += struct.pack('>f',c)
    geomData += struct.pack('>I', int(len(v) / 3))
    composite_list2 = vertexWeights
    for j in composite_list2:
        geomData+=struct.pack('>bbbbHHHH',j[0],j[1],j[2],j[3],j[4],j[5],j[6],j[7])

    # UINT WEIGHTCOUNT;
    # UNIMPLEMENTED #



    geomData += struct.pack('>bH13sH', 1, 13, 'character_mat'.encode('utf-8'), 0)
    # CHAR UNK; UINT STRINGLEN; CHAR[13] STRING; UINT STRINGLEN;
    geomData += struct.pack('>HH', int(len(tri) / 9), 770)
    # USHORT TRICOUNT; USHORT MODE;
    for x in tri:
        geomData += struct.pack('>h', int(x))
    crc = binascii.crc32(geomData[4:])
    geomData += struct.pack('>I', crc)
    file.write(geomData)
    # WRITE TO FILE

def NodeWrite():
    nodeStart = struct.pack('>I',168)

    nodeStart += struct.pack('>4sHH9sHHHBhhhhhffffffH4sH9sHHBhhhhhffffffH4sH4sH4sH4sHH13sH13sH',"NODE".encode('utf-8'), 3, 9, "CHARACTER".encode('utf-8'), 0, 0, 1, 0, 0, 0, 0, 0, 32512, 0, 0, 0, 1, 1, 1, 4, "ROOT".encode('utf-8'), 9, "CHARACTER".encode('utf-8'), 0, 1, 0, 0, 0, 0, 0, 32512, 0, 0, 0, 1, 1, 1, 4, "main".encode('utf-8'), 4, "ROOT".encode('utf-8'), 1, "GEOM".encode(), 4, "main".encode('utf-8'), 1, 13, "character_mat".encode('utf-8'), 13, "character_mat".encode('utf-8'), 0)
    #fout.write(nodePacked)
    crcNODE = binascii.crc32(nodeStart[4:])
    #nodePacked += struct.pack('BBBB',216, 44, 226, 217)
    #fout.write(nodecrc)
    nodeStart += struct.pack('>I',crcNODE)
    file.write(nodeStart)
def node2(geomnames,allbones):
    str1 = ''.join(geomnames)
    textsize = 0
    for k in allbones:
        print('? ',k[0],k[1])
        textsize = textsize+len(k[0])+len(k[1])
    calcsize = 2 + (len(geomnames)*46) + (len(str1)*2)+textsize+(len(allbones)*43)
    nodePacked = struct.pack('>I4sH',calcsize,'NODE'.encode('utf-8'),len(geomnames)+len(allbones))
    for y in allbones:
        nodePacked+= struct.pack('>H',len(y[0]))
        for str in y[0]:
            nodePacked += struct.pack('>c', bytes(str,encoding='utf-8'))
        nodePacked += struct.pack('>H', len(y[1]))
        for str in y[1]:
            nodePacked += struct.pack('>c', bytes(str,encoding='utf-8'))
        #print('test')
        print(y)
        rotx = float(y[2])
        roty = float(y[3])
        rotz = float(y[4])
        rotw = float(y[5])
        nodePacked += struct.pack('>HHbHhhhhffffff', 0,1,0,0,int(rotx*32512),int(roty*32512),int(rotz*32512),int(rotw*32512),y[6],y[7],y[8],y[9],y[10],y[11])
    for x in geomnames:
        print(x)
        nodePacked += struct.pack('>H',len(x))
        for c in x:
            nodePacked += struct.pack('s',bytes(c,encoding='utf-8'))
        nodePacked += struct.pack('>HH4sH',0,1,'CONT'.encode('utf-8'),len(x))
        for c in x:
            nodePacked += struct.pack('s',bytes(c,encoding='utf-8'))
        nodePacked += struct.pack('>HH13sH13sH', 1,13,'character_mat'.encode('utf-8'),13,'character_mat'.encode('utf-8'),0)

    crcNODE = binascii.crc32(nodePacked[4:])
    nodePacked += struct.pack('>I', crcNODE)
    file.write(nodePacked)

def wend():
    wendData = struct.pack('>I4s',0,'WEND'.encode('utf-8'))
    crc = binascii.crc32(wendData[4:])
    wendData += struct.pack('>I',crc)
    file.write(wendData)
    print("done at " + path)

#head()
#geom("cool", [1, 2, 3, 3, 2, 1], [5, 5, 5, 5, 5, 1], [1, 2, 2, 3], [1, 1, 1, 1, 1, 1, 1, 1, 1])
#node2(['name'])
#NodeWrite()
#wend()
