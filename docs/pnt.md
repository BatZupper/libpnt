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
    uint8_t md5[16];
    uint32_t data_size;
    uint8_t data[data_size];
};

```

wich they look like this. Also the magic number is clear with is __"PNT "__ (50 4E 54 00 exadecimal).

The format uses the md5 for integrity using 4 bytes per pixel.

the compression is a simple raw inflate of a targa file (without a header)

## Decompressing

for decompressing the library only handle the parsing of the pnt and image header but as soon as i manage to decompress even a pixel of data i will put it in the library

## Compressing

I still have to write code for this part. I could make a siple header maker but it isn't worth it yet
