#include <stdio.h>

#include "libpnt/libpnt.h"

int main(int argc, char *argv[]) {

    if(argc < 2) {
        puts("Not enough arguements");
        return 1;
    }

    FILE* pntfile = fopen(argv[1], "rb");

    if(pntCheck(pntfile) == 1) {
        puts("file is not a PNT");
        return 1;
    }

    PaintFileHeader header = getPNTHeader(pntfile);
    printf("magic number: %s basename: %s count: %u\n", header.magic, header.basename, header.count);
    ImageHeader image0 = getPNTImageHeader(pntfile, 0);
    printf("filename: %s height: %u width: %u metadata: %s data_size: %u\n", image0.filename, image0.height, image0.width, image0.metadata, image0.data_size);
    ImageHeader image1 = getPNTImageHeader(pntfile, 1);
    printf("filename: %s height: %u width: %u metadata: %s data_size: %u\n", image1.filename, image1.height, image1.width, image1.metadata, image1.data_size);
    ImageHeader image2 = getPNTImageHeader(pntfile, 2);
    printf("filename: %s height: %u width: %u metadata: %s data_size: %u\n", image2.filename, image2.height, image2.width, image2.metadata, image2.data_size);
    ImageHeader image3 = getPNTImageHeader(pntfile, 3);
    printf("filename: %s height: %u width: %u metadata: %s data_size: %u\n", image3.filename, image3.height, image3.width, image3.metadata, image3.data_size);
    return 0;
}