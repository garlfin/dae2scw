import struct
import binascii
file = open("scw/daeanim.scw", "wb")


def head():
    headData = struct.pack('>4s', 'SC3D'.encode('utf-8'))
    # CHAR[4] MAGIC;
    headData2 = struct.pack('>I4shhhhHb',11 , 'HEAD'.encode('utf-8'), 2, 30, 0, 39, 0, 0)
    # UINT ITEMSIZE; CHAR[4] ITEMTYPE; SHORT UNK; SHORT UNK1; SHORT UNK2; SHORT UNK3; USHORT STRINGLEN; CHAR[28] STRING; CHAR[0] REMAINING; UINT CRC;
    crc = binascii.crc32(headData2[4:])
    # CRC
    headData2 += struct.pack('>I', crc)
    # JOIN CRC TO MAIN STRUCT
    headData += headData2
    # JOIN STRUCTS
    file.write(headData)
    # WRITE TO FILE

def node2(allbones):

    textsize = 0
    animSize =0
    for k in allbones:
        print('? ',k[0],k[1])
        textsize = textsize+len(k[0])+len(k[1])
        animSize = animSize+len(k[2])*34
    calcsize = 2 +textsize+(len(allbones)*9)+animSize
    nodePacked = struct.pack('>I4sH',calcsize,'NODE'.encode('utf-8'),+len(allbones))
    for y in allbones:
        nodePacked+= struct.pack('>H',len(y[0]))
        for str in y[0]:
            nodePacked += struct.pack('>c', bytes(str,encoding='utf-8'))
        nodePacked += struct.pack('>H', len(y[1]))
        for str in y[1]:
            nodePacked += struct.pack('>c', bytes(str,encoding='utf-8'))
        #print('test')
        nodePacked += struct.pack('>HH',0,len(y[2]))
        nodePacked += b'\x7F'
        #print(y[2])
        for gmod in range(0,len(y[2])):
            current = y[2][gmod]
            print(current)
            nodePacked += struct.pack('>Hhhhhffffff', gmod+1,current[0],current[1],current[2],current[3],current[4],current[5],current[6],current[7],current[8],current[9])
            #nodePacked += struct.pack('>Hhhhhffffff', gmod + 1, 0, 0, 0, 0,
                                      #current[4], current[5], current[6], current[7], current[8], current[9])

        print('')


    crcNODE = binascii.crc32(nodePacked[4:])
    nodePacked += struct.pack('>I', crcNODE)
    file.write(nodePacked)



def wend():
    wendData = struct.pack('>I4s',0,'WEND'.encode('utf-8'))
    crc = binascii.crc32(wendData[4:])
    wendData += struct.pack('>I',crc)
    file.write(wendData)