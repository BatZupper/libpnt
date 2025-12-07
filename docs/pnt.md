# PiBoSo Paint (.pnt) File format

the .pnt file format is a format shared across all of the PiBoSo games like Mx Bikes, GP Bikes ect. The file is a propetary format that can only be made using the [Painted](https://docs.piboso.com/wiki/index.php/MXB_PaintEd) program wich let's keep this between us but it SUCK ASS so driven by this and by the curiosity on how this work i decided to reverse engineer the format and a bit of the program to better understand the file itself.

## Structure

the structure is still not completely clear we already know the header and some sort of entry/secondary header for each image in the paint

```C
struct PaintFileHeader {
    char magic[4]; //PNT 0x00
    char basename[100];
    uint32_t count;
};

struct PaintEntry {
    char filename[100];
    uint32_t width;
    uint32_t height;
    uint8_t metadata[16]; //MD5 algorithm
    uint32_t data_size;
    uint8_t data[data_size];
};

```

wich they look like this. Also the magic number is clear with is __"PNT "__ (50 4E 54 00 exadecimal) and looking at the code the compression might be something GZIP based but I'm not entirely sure yet.

Fpr the 16 bytes metadata array looking at the code is probably some encoded version of the words of the MD5 algorithm

## Decompressing

for decompressing due to the limited knowledge on the format i only made a header parser in python

```Py
import os
import struct
import zlib
from PIL import Image
import sys

def read_c_string(raw):
    return raw.split(b"\x00", 1)[0].decode(errors="ignore")

def extract_pnt(path):
    with open(path, "rb") as f:
        signature = f.read(4) #PNT 

        base_name_raw = f.read(100)
        base_name = read_c_string(base_name_raw)

        num_images = struct.unpack("<I", f.read(4))[0]

        print("File:", path)
        print("Base name:", base_name)
        print("Images:", num_images)

    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read_header.py <file.pnt>")
        sys.exit(1)

    pnt_file = sys.argv[1]
    extract_pnt(pnt_file)
```

i could also make the parse for Entry/Second header but i want to focus more on the decomp

## Compressing

I still have to write code for this part. I could make a siple header maker but it isn't worth it yet
