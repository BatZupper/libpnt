# libpnt

A simple C library for the PiBoSo paint file format (.pnt)

## Progress

at the moment the library can fully work with the headers but it can't extract the images or work some encrypted metadata yet

- [x] Set up the headers structure
- [x] Check if it's a valid pnt
- [x] Get the pnt header
- [x] Get the first image header
- [x] Get image header by index
- [ ] Work with the 16 byte image metadata
- [ ] Extract first image
- [ ] Extract image by index

## Documentation

The documentation related to the usage of the library is [here](docs/usage.md)
The documentation related to the file format is [here](docs/pnt.md)
