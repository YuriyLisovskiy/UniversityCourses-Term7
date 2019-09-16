#include "rle.h"

__RLE_INTERNAL_BEGIN__

bool compare(PIXEL px1, PIXEL px2)
{
	return px1.red == px2.red && px1.green == px2.green && px1.blue == px2.blue;
}

bool is_uncompressed_24_bits(BITMAP_INFO_HEADER info)
{
	if (info.bit_count != 24 || info.compression != 0)
	{
		std::cout << "This does not appear to be a 24-bit uncompressed bitmap.\n";
		return false;
	}

	return true;
}

void write_compressed_pixel(std::fstream& file, PIXEL px, uint32_t repetition)
{
	file.write((char*) &repetition, sizeof(repetition));
	file.write((char*) &px, sizeof(px));
}

void read_headers(std::fstream& file, BITMAP_FILE_HEADER& head, BITMAP_INFO_HEADER& info)
{
	// Read the headers to source file
	file.read((char*) &head, sizeof(struct internal::BITMAP_FILE_HEADER));
	file.read((char*) &info, sizeof(struct internal::BITMAP_INFO_HEADER));
}

void write_headers(std::fstream& file, BITMAP_FILE_HEADER head, BITMAP_INFO_HEADER info)
{
	// Write the headers to the output file
	file.write((char*) &head, sizeof(struct internal::BITMAP_FILE_HEADER));
	file.write((char*) &info, sizeof(struct internal::BITMAP_INFO_HEADER));
}

void assert_file_is_open(std::fstream& file, const std::string& name)
{
	if (!file.is_open())
	{
		std::cout << "Unable to open file '" << name << "'\n";
		exit(-1);
	}
}

__RLE_INTERNAL_END__


__RLE_BEGIN__

void bmp_compress(const std::string& input_file, const std::string& out_file)
{
	std::fstream in, out;

	in.open(input_file, std::ios::in | std::ios::binary);
	internal::assert_file_is_open(in, input_file);

	out.open(out_file, std::ios::out | std::ios::binary);
	internal::assert_file_is_open(out, out_file);

	// Store file header
	struct internal::BITMAP_FILE_HEADER source_head{};

	// Store bitmap info header
	struct internal::BITMAP_INFO_HEADER source_info{};

	internal::read_headers(in, source_head, source_info);

	if (!internal::is_uncompressed_24_bits(source_info))
	{
		in.close();
		out.close();

		exit(-1);
	}

	internal::write_headers(out, source_head, source_info);

	uint32_t repetition = 1;
	internal::PIXEL current, next;

	in.read((char*) &current, sizeof(internal::PIXEL));
	in.read((char*) &next, sizeof(internal::PIXEL));

	size_t i = 0;
	size_t totalPixels = source_info.width * source_info.height;

	while (i < totalPixels)
	{
		if (!compare(current, next))
		{
			internal::write_compressed_pixel(out, current, repetition);
			repetition = 1;
		}
		else
		{
			repetition++;
		}

		current = next;
		in.read((char*) &next, sizeof(internal::PIXEL));
		i++;
	}

	internal::write_compressed_pixel(out, current, repetition);

	std::cout << in.tellg() << " bytes compressed into " << out.tellg() << " bytes.\n";

	in.close();
	out.close();
}

void bmp_decompress(const std::string& input_file, const std::string& out_file)
{
	std::fstream in, out;

	in.open(input_file, std::ios::in | std::ios::binary);
	internal::assert_file_is_open(in, input_file);

	out.open(out_file, std::ios::out | std::ios::binary);
	internal::assert_file_is_open(out, out_file);

	// Store file header
	struct internal::BITMAP_FILE_HEADER source_head{};

	// Store bitmap info header
	struct internal::BITMAP_INFO_HEADER source_info{};

	internal::read_headers(in, source_head, source_info);
	internal::write_headers(out, source_head, source_info);

	size_t totalPixels = source_info.width * source_info.height;

	size_t i = 0;
	uint32_t pixelRepetition = 0;
	internal::PIXEL pixel;

	while (i < totalPixels)
	{
		in.read((char*) &pixelRepetition, sizeof(pixelRepetition));
		in.read((char*) &pixel, sizeof(pixel));

		for (size_t j = 0; j < pixelRepetition; j++)
		{
			out.write((char*) &pixel, sizeof(pixel));
			i++;
		}
	}

	out.write((char*) &pixel, sizeof(pixel));

	std::cout << in.tellg() << " bytes decompressed into " << out.tellg() << " bytes.\n";

	in.close();
	out.close();
}

__RLE_END__
