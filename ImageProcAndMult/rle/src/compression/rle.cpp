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

int get_file_size(const std::string& path)
{
	std::fstream f;
	f.open(path, std::ios::in | std::ios::ate | std::ios::binary);
	return f.tellg();
}

__RLE_INTERNAL_END__

#define READING "reading"
#define WRITING "writing"
#define ENCODING "encoding"
#define DECODING "decoding"

__RLE_BEGIN__

void bmp_compress(const std::string& input_file, const std::string& out_file, TimingData& td)
{
	TimeTracker tracker;

	tracker.start(READING);
	std::fstream in;
	in.open(input_file, std::ios::in | std::ios::binary);
	internal::assert_file_is_open(in, input_file);

	// Store file header
	struct internal::BITMAP_FILE_HEADER source_head{};

	// Store bitmap info header
	struct internal::BITMAP_INFO_HEADER source_info{};

	internal::read_headers(in, source_head, source_info);

	if (!internal::is_uncompressed_24_bits(source_info))
	{
		in.close();
		exit(-1);
	}

	uint32_t repetition = 1;
	internal::PIXEL next{};

	std::vector<internal::PIXEL> pixels{};
	while (!in.eof())
	{
		in.read((char*) &next, sizeof(internal::PIXEL));
		pixels.push_back(next);
	}
	in.close();
	td.reading_time += tracker.elapsed(READING);

	tracker.start(ENCODING);
	internal::PIXEL current = pixels.front();
	pixels.erase(pixels.begin());

	std::vector<std::pair<internal::PIXEL, uint32_t>> compressed_pixels{};
	for (const auto& pixel : pixels)
	{
		if (!compare(current, pixel))
		{
			compressed_pixels.emplace_back(current, repetition);
			repetition = 1;
		}
		else
		{
			repetition++;
		}

		current = pixel;
	}
	td.encoding_time += tracker.elapsed(ENCODING);

	tracker.start(WRITING);
	std::fstream out;
	out.open(out_file, std::ios::out | std::ios::binary);
	internal::assert_file_is_open(out, out_file);

	internal::write_headers(out, source_head, source_info);

	for (const auto& compressed_pixel : compressed_pixels)
	{
		internal::write_compressed_pixel(out, compressed_pixel.first, compressed_pixel.second);
	}

	out.close();
	td.writing_time += tracker.elapsed(WRITING);

	std::cout << internal::get_file_size(input_file) << " bytes compressed into " << internal::get_file_size(out_file) << " bytes.\n";
}

void bmp_decompress(const std::string& input_file, const std::string& out_file, TimingData& td)
{
	TimeTracker tracker;

	tracker.start(READING);
	std::fstream in;
	in.open(input_file, std::ios::in | std::ios::binary);
	internal::assert_file_is_open(in, input_file);

	// Store file header
	struct internal::BITMAP_FILE_HEADER source_head{};

	// Store bitmap info header
	struct internal::BITMAP_INFO_HEADER source_info{};

	internal::read_headers(in, source_head, source_info);

	uint32_t pixelRepetition = 0;
	internal::PIXEL pixel{};

	std::vector<std::pair<internal::PIXEL, uint32_t>> compressed_pixels{};
	while (!in.eof())
	{
		in.read((char*) &pixelRepetition, sizeof(uint32_t));
		in.read((char*) &pixel, sizeof(internal::PIXEL));

		compressed_pixels.emplace_back(pixel, pixelRepetition);
	}
	in.close();
	td.reading_time += tracker.elapsed(READING);

	tracker.start(DECODING);
	std::vector<internal::PIXEL> pixels{};
	for (const auto& compressed_pixel : compressed_pixels)
	{
		for (size_t j = 0; j < compressed_pixel.second; j++)
		{
			pixels.push_back(compressed_pixel.first);
		}
	}
	td.decoding_time += tracker.elapsed(DECODING);

	tracker.start(WRITING);
	std::fstream out;
	out.open(out_file, std::ios::out | std::ios::binary);
	internal::assert_file_is_open(out, out_file);

	internal::write_headers(out, source_head, source_info);

	for (const auto& px : pixels)
	{
		out.write((char*) &px, sizeof(pixel));
	}

	out.close();
	td.writing_time += tracker.elapsed(WRITING);

	std::cout << internal::get_file_size(input_file) << " bytes decompressed into " << internal::get_file_size(out_file) << " bytes.\n";
}

__RLE_END__
