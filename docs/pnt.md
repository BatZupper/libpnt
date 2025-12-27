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

struct ImageHeader {
    char filename[100];
    uint32_t width;
    uint32_t height;
    uint8_t md5[16];
    uint32_t data_size;
    //8 bytes padding
    uint8_t data[data_size];
};

```

starting by the paint header this is really straight forward it just contains the magic number, name of the paint wich has to be a fixed size of 100. If the actual name is smaller it just fills it with empty bytes and at the last the count of the images saved as a unsigned int.

Now looking at the Image Header this has a few more stuff starting with the image file name without the extention again here it has to be a fixed size of 100 bytes, then pretty standard width and height both saved as unsigned ints then there's a MD5 checksum. The checksum is calculated by using this calculating the total number of pixer times the bytes per pixels (4 bytes per pixels). After that the file size + 8 bytes because there's a 8 bytes padding after the data size afther that the compressed image data. This header is written for each of the images in the file.

The uncompressed data strutture is a TGA file without both the header and the footer. The data inside the tga is stored following the BGRA (Blu Green Red Alpha) format. Then the data is compressed using the raw deflate tecnology  

## Decompressing

For decompressing the file the library very simply take the image (specified by index) uncompress the data using raw deflate then converting the BGRA into a more standard RGBA and then recreate the TGA header using the information from the Image header in the paint file

## Compressing

For compressing i basically just do the decompressing process but inverted with a few extra steps. First it recreates the magic number and using user input the paint name then it counts the tga files in the directory specified by user input and puts the number in the paint header. Then for each image using the information in the TGA header (specifically width and height) then calculates the cheksum using the total number of pixer times the bytes per pixels (4 bytes per pixels) with the MD5 algorithm then removes the header and footer then converts the data from RGBA to BGRA and compress it using the raw deflate algorith.
