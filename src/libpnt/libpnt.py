import zlib
import struct
import os
import hashlib

#declare the PNT related constants
PNT_MAGIC_NUMBER = b"PNT\x00"
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
#declare the TGA related constants
TGA_HEADER_SIZE = 18
TGA_FOOTER_SIZE = 26

class PaintFileHeader:
    def __init__(self):
        self.magic = ""
        self.basename = ""
        self.count = 0

    def __str__(self):
        return f"Magic Number: {self.magic}\nBasename: {self.basename}\nCount: {self.count}"

class ImageHeader:
    def __init__(self):
        self.filename = ""
        self.width = 0
        self.height = 0
        self.md5 = []
        self.data_size = 0

    def __str__(self):
        return f"Filename: {self.filename}\nWidth: {self.width}\nHeight: {self.height}\nMD5: {self.md5}\nData Size: {self.data_size}"

#check if it's a valid PNT file
def pntCheck(pntFile):
    check = pntFile.read(MAGIC_NUMBER_SIZE) == PNT_MAGIC_NUMBER
    pntFile.seek(0)
    return check

#get the paint file header
def getPNTHeader(pntFile):
    header = PaintFileHeader()
    header.magic = pntFile.read(MAGIC_NUMBER_SIZE)
    header.basename = pntFile.read(BASENAME_SIZE).decode('ascii', errors='ignore').rstrip('\x00')
    header.count = int.from_bytes(pntFile.read(COUNT_SIZE), 'little')
    pntFile.seek(0)
    return header

#get the image header (specified by index)
def getImageHeader(pntFile, index):
    imageHeader = ImageHeader()
    pntFile.seek(HEADER_SIZE)

    for i in range(index + 1):
        #update all of the info
        filename = pntFile.read(IMAGE_FILENAME_SIZE)
        width = pntFile.read(IMAGE_WIDTH_SIZE)
        height = pntFile.read(IMAGE_HEIGHT_SIZE)
        md5 = pntFile.read(IMAGE_MD5_SIZE)
        data_size = int.from_bytes(pntFile.read(IMAGE_DATA_SIZE_SIZE), "little")

        if i != index:
            #if not the right image skip
            pntFile.seek(data_size, 1)
        else:
            #set the temp header
            imageHeader.filename = filename.decode('ascii', errors='ignore').rstrip('\x00')
            imageHeader.width = int.from_bytes(width, "little")
            imageHeader.height = int.from_bytes(height, "little")
            imageHeader.md5 = md5
            imageHeader.data_size = data_size

    pntFile.seek(0)
    return imageHeader

#decompress image (specified by index) and returns the decompressed data
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
            #set the tga header
            tgaHeader = struct.pack("<BBBHHBHHHHBB", 0, 0, 2, 0, 0, 0, 0, 0, width, height, 32, 8)
            pntFile.seek(0)
            data = bytearray(decompressedData)
            #convert bgra to rgba
            for i in range(0, len(data), 4):
                b = data[i]
                g = data[i+1]
                r = data[i+2]
                a = data[i+3]

                data[i]   = r
                data[i+1] = g
                data[i+2] = b
                data[i+3] = a  
            decompressedData = bytes(data)

            return tgaHeader + decompressedData

def compressImage(imagePath):
    imageSize = os.path.getsize(imagePath)
    tgaFile = open(imagePath, "rb")
    tgaFile.seek(TGA_HEADER_SIZE, 0)
    uncompressedData = tgaFile.read(imageSize - TGA_FOOTER_SIZE - TGA_HEADER_SIZE)
    data = bytearray(uncompressedData)
    #rgba to bgra
    for i in range(0, len(data), 4):
        r = data[i]
        g = data[i+1]
        b = data[i+2]
        a = data[i+3]

        data[i]   = b
        data[i+1] = g
        data[i+2] = r
        data[i+3] = a

    uncompressedData = bytes(data)

    compressedData = zlib.compress(uncompressedData, 9, -15)
    tgaFile.close()
    return compressedData

def createPaintFile(imagesPath, paintName):
    md5 = hashlib.md5()
    with open("test.bin", "wb") as f:
        #create PNT header
        f.write(PNT_MAGIC_NUMBER)
        f.write(paintName.encode("ascii"))
        f.write(b"\x00" * (100 - len(paintName)))
        f.write(b"\x01\x00\x00\x00") #TODO subsitute with actual image number
        #TODO do it also with multiple images
        #create image header
        f.write(imagesPath[:-4].encode("ascii"))
        f.write(b"\x00" * (104 - len(imagesPath))) # 100 basename bytes + 4 of the .tga removed (i need to fucking rewrite the whole thing)
        with open(imagesPath, "rb") as tga:
            tga.seek(12) #distance in the header between the start and the size
            width = int.from_bytes(tga.read(2), "little")
            height = int.from_bytes(tga.read(2), "little")
            #create MD5 checksum
            md5.update(int.to_bytes(width * height * 4, 8))
            f.write(width.to_bytes(4, byteorder='little'))
            f.write(height.to_bytes(4, byteorder='little'))
            f.write(md5.digest())
        compressedData = compressImage(imagesPath)
        f.write((len(compressedData) + 8).to_bytes(4, "little"))
        f.write(b"\x00" * 8)
        f.write(compressedData)