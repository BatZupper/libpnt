#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "libpnt.h"

//check if the magic number is correct. If it is returns 0 otherwise 1
int pntCheck(FILE* pntFile) {
    char magicNumber[4];
    size_t bytesRead = fread(magicNumber, 1, MAGIC_NUMBER_SIZE, pntFile);
    //after reading set the offset to 0
    fseek(pntFile, 0, SEEK_SET);
    //check if the size of the header is correct
    if(bytesRead < MAGIC_NUMBER_SIZE)
        return 1;
    //check if the magic number is correct
    if (magicNumber[0] == 'P' && magicNumber[1] == 'N' && magicNumber[2] == 'T' && magicNumber[3] == 0x00) 
        return 0;
    //if the check fails trow an error
    else
        return 1;
    
    //if anything goes wrong just throw an error
    return 1;
}

//get the header from the paint file
PaintFileHeader getPNTHeader(FILE* pntFile) {
    PaintFileHeader tempHeader;
    char buffer[108];
    size_t bytesRead = fread(buffer, 1, HEADER_SIZE, pntFile);
    //if the bytes read are too little return nothing
    if(bytesRead < HEADER_SIZE) {
        memset(&tempHeader, 0, sizeof(PaintFileHeader));
        return tempHeader;
    }
    //populate the temporary header
    memcpy(tempHeader.magic, buffer, MAGIC_NUMBER_SIZE);
    memcpy(tempHeader.basename, buffer + MAGIC_NUMBER_SIZE, BASENAME_SIZE);
    memcpy(&tempHeader.count, buffer + HEADER_SIZE - COUNT_SIZE, COUNT_SIZE);
    //return the header
    return tempHeader;
}

//get the header of the image specified by the index in the paint file
ImageHeader getPNTImageHeader(FILE* pntFile, int index) {
    // Calculate file dimension
    fseek(pntFile, 0, SEEK_END);
    long fileSize = ftell(pntFile);
    fseek(pntFile, 0, SEEK_SET);
    // read the file in memory
    char* buffer = malloc(fileSize);
    fread(buffer, 1, fileSize, pntFile);

    char* ptr = buffer + HEADER_SIZE;

    for (int i = 0; i < index; i++) {
        ptr += IMAGE_HEADER_SIZE - 4;        // skip header
        long dataSize;
        memcpy(&dataSize, ptr, 4);       // read dataSize dimension
        ptr += 4 + dataSize;             // skip data
    }

    ImageHeader header;
    memcpy(header.filename, ptr, IMAGE_FILENAME_SIZE);
    ptr += IMAGE_FILENAME_SIZE;
    memcpy(&header.width, ptr, IMAGE_WIDTH_SIZE);
    ptr += IMAGE_WIDTH_SIZE;
    memcpy(&header.height, ptr, IMAGE_HEIGHT_SIZE);
    ptr += IMAGE_HEIGHT_SIZE;
    memcpy(&header.metadata, ptr, IMAGE_METADATA_SIZE);
    ptr += IMAGE_METADATA_SIZE;
    memcpy(&header.data_size, ptr, IMAGE_DATA_SIZE_SIZE);
    free(buffer);
    return header;
}
