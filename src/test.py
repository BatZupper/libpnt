import libpnt.libpnt as libpnt
import sys

# pntFile = open(sys.argv[1], "rb")

# if libpnt.pntCheck(pntFile) == True:
#     print("va bene procedo")

# pntHeader = libpnt.getPNTHeader(pntFile)

# print(pntHeader)
# index = 0
# while index <= pntHeader.count - 1:
#     imageHeader = libpnt.getImageHeader(pntFile, index)
#     with open(f"decompressed{index}.tga", "wb") as f:
#         f.write(libpnt.decompressImage(pntFile, index))
#     index += 1

# pntFile.close()

libpnt.createPaintFile(sys.argv[1], sys.argv[2])