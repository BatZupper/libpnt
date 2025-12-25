import libpnt.libpnt as libpnt

pntFile = open("YOURFILE", "rb")

if libpnt.pntCheck(pntFile) == True:
    print("va bene procedo")

pntHeader = libpnt.getPNTHeader(pntFile)

print(pntHeader.magic)
print(pntHeader.basename)
print(pntHeader.count)
index = 0
while index <= pntHeader.count - 1:
    imageHeader = libpnt.getImageHeader(pntFile, index)
    print(imageHeader.filename)
    print(imageHeader.width)
    print(imageHeader.height)
    print(imageHeader.md5)
    print(imageHeader.data_size)
    with open(f"decompressed{index}.tga", "wb") as f:
        f.write(libpnt.decompressImage(pntFile, index))
    index += 1

pntFile.close()
