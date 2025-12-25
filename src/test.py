import libpnt.libpnt as libpnt

pntFile = open("C:/Users/super/Desktop/progettirandom/libpnt/black.pnt", "rb")

if libpnt.pntCheck(pntFile) == True:
    print("va bene procedo")

pntHeader = libpnt.getPNTHeader(pntFile)

print(pntHeader.magic)
print(pntHeader.basename)
print(pntHeader.count)

imageHeader = libpnt.getImageHeader(pntFile, 0)

print(imageHeader.filename)
print(imageHeader.width)
print(imageHeader.height)
print(imageHeader.md5)
print(imageHeader.data_size)

with open("decompressed.tga", "wb") as f:
    f.write(libpnt.decompressImage(pntFile, 0))

pntFile.close()
