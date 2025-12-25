import zlib
import struct

#all the constants
MAGIC_NUMBER_SIZE = 4
BASENAME_SIZE = 100
COUNT_SIZE = 4
HEADER_SIZE = 108
IMAGE_HEADER_SIZE = 128
IMAGE_FILENAME_SIZE = 100
IMAGE_WIDTH_SIZE = 4
IMAGE_HEIGHT_SIZE = 4
IMAGE_MD5_SIZE = 16
IMAGE_DATA_SIZE_SIZE = 4 #this shit is ridiculus (yes i had to copy the exact commenct)
IMAGE_PADDING = 8

class PaintFileHeader:
    def __init__(self):
        self.magic = ""
        self.basename = ""
        self.count = 0

class ImageHeader:
    def __init__(self):
        self.filename = ""
        self.width = 0
        self.height = 0
        self.md5 = []
        self.data_size = 0

def pntCheck(pntFile):
    check = pntFile.read(MAGIC_NUMBER_SIZE) == b"PNT\x00"
    pntFile.seek(0)
    return check
    
def getPNTHeader(pntFile):
    header = PaintFileHeader()
    header.magic = pntFile.read(MAGIC_NUMBER_SIZE)
    header.basename = pntFile.read(BASENAME_SIZE).decode('ascii').rstrip('\x00')
    header.count = int.from_bytes(pntFile.read(COUNT_SIZE), 'little')
    pntFile.seek(0)
    return header

def getImageHeader(pntFile, index):
    imageHeader = ImageHeader()
    pntFile.seek(HEADER_SIZE)

    for i in range(index + 1):
        filename = pntFile.read(IMAGE_FILENAME_SIZE)
        width = pntFile.read(IMAGE_WIDTH_SIZE)
        height = pntFile.read(IMAGE_HEIGHT_SIZE)
        md5 = pntFile.read(IMAGE_MD5_SIZE)
        data_size = int.from_bytes(pntFile.read(IMAGE_DATA_SIZE_SIZE), "little")

        if i != index:
            pntFile.seek(data_size + IMAGE_PADDING, 1)
        else:
            imageHeader.filename = filename.decode('ascii').rstrip('\x00')
            imageHeader.width = int.from_bytes(width, "little")
            imageHeader.height = int.from_bytes(height, "little")
            imageHeader.md5 = md5
            imageHeader.data_size = data_size

    return imageHeader

def decompressImage(pntFile, index):
    pntFile.seek(HEADER_SIZE)

    for i in range(index + 1):
        pntFile.seek(IMAGE_FILENAME_SIZE, 1)
        width = int.from_bytes(pntFile.read(IMAGE_WIDTH_SIZE), "little")
        height = int.from_bytes(pntFile.read(IMAGE_HEIGHT_SIZE), "little")
        pntFile.seek(IMAGE_MD5_SIZE, 1)
        data_size = int.from_bytes(pntFile.read(IMAGE_DATA_SIZE_SIZE), "little")

        if i != index:
            pntFile.seek(data_size, 1)
        else:
            pntFile.seek(IMAGE_PADDING, 1)
            compressedData = pntFile.read(data_size - 8)
            decompressedData = zlib.decompress(compressedData, -15)
            tgaHeader = struct.pack("<BBBHHBHHHHBB", 0, 0, 2, 0, 0, 0, 0, 0, width, height, 32, 8)
            return tgaHeader + decompressedData