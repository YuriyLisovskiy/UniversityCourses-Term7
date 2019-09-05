#ifndef UNI7_RLE_H
#define UNI7_RLE_H

#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <iostream>
#include <fstream>

#define __RLE_BEGIN__ namespace rle {
#define __RLE_END__ }

#define __RLE_INTERNAL_BEGIN__ __RLE_BEGIN__ namespace internal {
#define __RLE_INTERNAL_END__ } __RLE_END__

__RLE_INTERNAL_BEGIN__

// structure defines bitmap header
struct BITMAP_FILE_HEADER
{
	uint8_t type[2];        // type of file (bit map)
	uint32_t size;          // size of file
	uint16_t reserved_1;
	uint16_t reserved_2;
	uint32_t offset_bits;    //off set bits

} __attribute__ ((packed));

struct BITMAP_INFO_HEADER
{
	uint32_t size;          // bitmap size
	// uint16_t w2;
	uint32_t width;         // width of bitmap
	//uint16_t h2;
	uint32_t height;        // height of bitmap

	uint16_t planes;
	uint16_t bit_count;
	uint32_t compression;   // compression ratio (zero for no compression)
	uint32_t size_image;    // size of image
	long x_pels_per_meter;
	long y_pels_per_meter;
	uint32_t colors_used;
	uint32_t colors_important;

} __attribute__ ((packed));

typedef struct SINGLE_PIXEL
{
	uint8_t green;  // Green level 0-255
	uint8_t red;    // Red level 0-255
	uint8_t blue;   // Green level 0-255
} PIXEL;

extern bool compare(PIXEL px1, PIXEL px2);

extern bool is_uncompressed_24_bits(BITMAP_INFO_HEADER info);

extern void write_compressed_pixel(std::fstream& file, PIXEL px, uint32_t repetition);

extern void read_headers(std::fstream& file, BITMAP_FILE_HEADER& head, BITMAP_INFO_HEADER& info);

extern void write_headers(std::fstream& file, BITMAP_FILE_HEADER head, BITMAP_INFO_HEADER info);

extern void assert_file_is_open(std::fstream& file, const std::string& name);

__RLE_INTERNAL_END__

__RLE_BEGIN__

extern void bmp_compress(const std::string& input_file, const std::string& out_file);

extern void bmp_decompress(const std::string& input_file, const std::string& out_file);

__RLE_END__

#endif // UNI7_RLE_H
