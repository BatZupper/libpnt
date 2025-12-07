#include <stdio.h>
#include <stdint.h>

//define all the constans
#define MAGIC_NUMBER_SIZE 4
#define BASENAME_SIZE 100
#define COUNT_SIZE 4
#define HEADER_SIZE 108
#define IMAGE_HEADER_SIZE 128
#define IMAGE_FILENAME_SIZE 100
#define IMAGE_WIDTH_SIZE 4
#define IMAGE_HEIGHT_SIZE 4
#define IMAGE_METADATA_SIZE 16
#define IMAGE_DATA_SIZE_SIZE 4 //this shit is ridiculus

//define the header of the paint file
typedef struct {
    char magic[4];    // PNT 0x00
    char basename[100];
    uint32_t count;
} PaintFileHeader;

//define header of the image
typedef struct {
    char filename[100];
    uint32_t width;
    uint32_t height;
    uint8_t metadata[16]; //MD5 algorithm
    uint32_t data_size;
    uint8_t *data;
} ImageHeader;

//declare the functions
int pntCheck(FILE* pntFile);
PaintFileHeader getPNTHeader(FILE* pntFile);
ImageHeader getPNTImageHeader(FILE* pntFile, int index);