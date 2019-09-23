#include "rle.h"

/*

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
	file.write((char*) &repetition, sizeof(uint32_t));
	file.write((char*) &px, sizeof(PIXEL));
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

	std::vector<internal::PIXEL> pixels{};
	internal::PIXEL next;
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

	bool write_last = false;
	uint32_t repetition = 1;

	for (const auto& pixel : pixels)
	{
		if (!compare(current, pixel))
		{
			compressed_pixels.emplace_back(current, repetition);
			repetition = 0;
			write_last = false;
		}
		else
		{
			write_last = true;
		}

		repetition++;
		current = pixel;
	}

	if (write_last)
	{
		compressed_pixels.emplace_back(current, repetition);
	}

	td.encoding_time += tracker.elapsed(ENCODING);

	tracker.start(WRITING);
	std::fstream out;
	out.open(out_file, std::ios::out | std::ios::binary);
	internal::assert_file_is_open(out, out_file);

	// Set compression flag to 1 which means RLE 8-bit/pixel
//	source_info.compression = 1;

	internal::write_headers(out, source_head, source_info);

	for (const auto& compressed_pixel : compressed_pixels)
	{
		internal::write_compressed_pixel(out, compressed_pixel.first, compressed_pixel.second);
	}

	out.close();
	td.writing_time += tracker.elapsed(WRITING);

//	std::cout << internal::get_file_size(input_file) << " bytes compressed into " << internal::get_file_size(out_file) << " bytes.\n";
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

	// Remove compression flag
//	source_info.compression = 0;
	internal::write_headers(out, source_head, source_info);

	for (const auto& px : pixels)
	{
		out.write((char*) &px, sizeof(pixel));
	}

	out.close();
	td.writing_time += tracker.elapsed(WRITING);

//	std::cout << internal::get_file_size(input_file) << " bytes decompressed into " << internal::get_file_size(out_file) << " bytes.\n";
}

__RLE_END__
*/

__RLE_BEGIN__

#define READING "reading"
#define WRITING "writing"
#define ENCODING "encoding"
#define DECODING "decoding"

bool compare(PIXEL px1, PIXEL px2)
{
	return px1.red == px2.red && px1.green == px2.green && px1.blue == px2.blue;
}

int bmp_compress(const std::string& input_file, const std::string& out_file, TimingData& td)
{
	TimeTracker tracker;

	tracker.start(READING);
	std::fstream in;
	in.open(input_file, std::ios::in | std::ios::binary);

	// Reading the file
	auto* image = new _bitmap();
	in.read((char*) image, sizeof(_bitmap));

	// Controlling the magic number and the header size
	if (image->magicNumber[0] != 'B' || image->magicNumber[1] != 'M' || image->headerSize != 40 || image->depth != 24)
	{
		fprintf(stderr, "Error: Incompatible file type\n");
		free(image);
		return EXIT_FAILURE;
	}

	// Controlling the start offset
	if (image->startOffset < sizeof(_bitmap))
	{
		fprintf(stderr, "Error: Wrong start offset\n");
		free(image);
		return EXIT_FAILURE;
	}

	// Reading pixels
	std::vector<PIXEL> pixels{};
	PIXEL px;
	while (!in.eof())
	{
		in.read((char*) &px, sizeof(PIXEL));
		pixels.push_back(px);
	}
	in.close();
	td.reading_time = tracker.elapsed(READING);

	// RLE compression
	tracker.start(ENCODING);
	uint32_t total = 0, occurrences = 1;
	std::vector<std::pair<uint32_t, PIXEL>> data{};
	PIXEL current = pixels.front();
	pixels.erase(pixels.begin());
	for (const auto& next : pixels)
	{
		if (compare(current, next))
		{
			occurrences++;
		}
		else
		{
			data.emplace_back(occurrences, current);
			total += sizeof(uint32_t) + sizeof(PIXEL);

			occurrences = 1;
			current = next;
		}
	}

	// End of the last line
	data.emplace_back(occurrences, current);
	total += sizeof(uint32_t) + sizeof(PIXEL);
	td.encoding_time = tracker.elapsed(ENCODING);

	fprintf(stdout, "Compression ratio = %f%%\n", 100.0 - (image->startOffset + total) * 100.0 / image->size);

	// Writing the file
	tracker.start(WRITING);
	std::fstream out;
	out.open(out_file, std::ios::out | std::ios::binary);

	out.write((char*) image, sizeof(_bitmap));

	for (const auto& item : data)
	{
		out.write((char*) &item.first, sizeof(uint32_t));
		out.write((char*) &item.second, sizeof(PIXEL));
	}

	out.close();
	td.writing_time = tracker.elapsed(WRITING);

	free(image);

	return EXIT_SUCCESS;
}

int bmp_decompress(const std::string& input_file, const std::string& out_file, TimingData& td) {
	TimeTracker tracker;

	tracker.start(READING);
	std::fstream in;
	in.open(input_file, std::ios::in | std::ios::binary);

	// Reading the file
	auto* image = new _bitmap();
	in.read((char*) image, sizeof(_bitmap));

	// Controlling the magic number and the header size
	if (image->magicNumber[0] != 'B' || image->magicNumber[1] != 'M' || image->headerSize != 40 || image->depth != 24)
	{
		fprintf(stderr, "Error: Incompatible file type\n");
		free(image);
		return EXIT_FAILURE;
	}

	// Controlling the start offset
	if (image->startOffset < sizeof(_bitmap))
	{
		fprintf(stderr, "Error: Wrong start offset\n");
		free(image);
		return EXIT_FAILURE;
	}

	std::vector<std::pair<uint32_t, PIXEL>> compressed_data{};
	uint32_t occurrences, total = 0;
	PIXEL current;
	while (!in.eof())
	{
		in.read((char*) &occurrences, sizeof(uint32_t));
		in.read((char*) &current, sizeof(PIXEL));
		if (occurrences)
		{
			compressed_data.emplace_back(occurrences, current);
		}
	}
	in.close();
	td.reading_time = tracker.elapsed(READING);

	// RLE decompression
	tracker.start(DECODING);
	std::vector<PIXEL> pixels;
	for (const auto& compressed : compressed_data)
	{
		for (size_t j = 0; j < compressed.first; j++)
		{
			pixels.push_back(compressed.second);
			total += sizeof(PIXEL);
		}
	}
	td.decoding_time = tracker.elapsed(DECODING);

	// Writing the file
	tracker.start(WRITING);
	std::fstream out;
	out.open(out_file, std::ios::out | std::ios::binary);

	out.write((char*) image, sizeof(_bitmap));

	for (const auto& px : pixels)
	{
		out.write((char*) &px, sizeof(PIXEL));
	}
	out.close();
	td.writing_time = tracker.elapsed(WRITING);

	free(image);

	return EXIT_SUCCESS;
}

/*

const uint8_t lineFeed = 0x00;
const uint8_t imageEnd = 0x01;

int bmp_compress(const std::string& input_file, const std::string& out_file, TimingData& td)
{
	TimeTracker tracker;

	tracker.start(READING);
	std::fstream in;
	in.open(input_file, std::ios::in | std::ios::binary);

	uint32_t i, total = 0;
	_bitmap* image = nullptr;
	uint32_t occ = 0;
	PIXEL cur{}, cur2{};
	bool readRef = true;

	// Reading the file
	image = new _bitmap();
	in.read((char*) image, sizeof(_bitmap));

	// Controlling the magic number and the header size
	if (image->magicNumber[0] != 'B' || image->magicNumber[1] != 'M'
	    || image->headerSize != 40 || image->depth != 24
	    || image->compression)
	{
		fprintf(stderr, "Error: Incompatible file type\n");
		free(image);
		return EXIT_FAILURE;
	}

	// Controlling the start offset
	if (image->startOffset < sizeof(_bitmap))
	{
		fprintf(stderr, "Error: Wrong start offset\n");
		free(image);
		return EXIT_FAILURE;
	}

	// RLE compression
	std::vector<std::pair<uint32_t, PIXEL>> data{};

	for (i = 0; i < image->imageSize; i++)
	{
		// End of line
		if (i && !(i % image->width))
		{
			if (occ)
			{
				data.emplace_back(occ, cur);
				total += sizeof(uint32_t) + sizeof(PIXEL);
			}
			data.emplace_back(0x00, PIXEL{lineFeed, lineFeed, lineFeed});
			total += sizeof(uint32_t) + sizeof(PIXEL);

			occ = 0;
			readRef = true;
		}

		// Max occurences
		if (255 == occ)
		{
			data.emplace_back(occ, cur);
			total += sizeof(uint32_t) + sizeof(PIXEL);

			occ = 0;
			readRef = true;
		}

		if (readRef)
		{
			in.read((char*) &cur, sizeof(PIXEL));
			occ++;
			readRef = false;
		}
		else
		{
			in.read((char*) &cur2, sizeof(PIXEL));
			if (compare(cur, cur2)) {
				occ++;
			} else {
				data.emplace_back(occ, cur);
				total += sizeof(uint32_t) + sizeof(PIXEL);

				occ = 1;
				cur = cur2;
			}
		}
	}

	in.close();

	// End of the last line
	if (occ)
	{
		data.emplace_back(occ, cur);
		total += sizeof(uint32_t) + sizeof(PIXEL);
	}

	data.emplace_back(0x00, PIXEL{imageEnd, imageEnd, imageEnd});
	total += sizeof(uint32_t) + sizeof(PIXEL);

	fprintf(stdout, "Compression ratio = %f%%\n", 100.0 - (image->startOffset + total) * 100.0 / image->size);

	// Updating header informations
	image->imageSize = total;
	image->size = image->startOffset + image->imageSize;
	image->compression = 0x0001;

	// Writing the file
	std::fstream out;
	out.open(out_file, std::ios::out | std::ios::binary);

	out.write((char*) image, sizeof(_bitmap));

	for (const auto& item : data)
	{
		out.write((char*) &item.first, sizeof(uint32_t));
		out.write((char*) &item.second, sizeof(PIXEL));
	}

	out.close();

	free(image);

	return EXIT_SUCCESS;
}

int bmp_decompress(const std::string& input_file, const std::string& out_file, TimingData& td)
{
	TimeTracker tracker;

	tracker.start(READING);
	std::fstream in;
	in.open(input_file, std::ios::in | std::ios::binary);

	_bitmap* image = nullptr;
	uint32_t j, total = 0;

	// Reading the file
	image = new _bitmap();
	in.read((char*) image, sizeof(_bitmap));

	// Controlling the magic number and the header size
	if (image->magicNumber[0] != 'B' || image->magicNumber[1] != 'M'
	    || image->headerSize != 40 || image->depth != 24
	    || image->compression != 1)
	{
		fprintf(stderr, "Error: Incompatible file type\n");
		free(image);
		return EXIT_FAILURE;
	}

	// Controlling the start offset
	if (image->startOffset < sizeof (_bitmap))
	{
		fprintf(stderr, "Error: Wrong start offset\n");
		free(image);
		return EXIT_FAILURE;
	}

	// RLE decompression
	std::vector<PIXEL> data;
	uint32_t occ;
	PIXEL cur;

	while (!in.eof())
	{
		in.read((char*) &occ, sizeof(uint32_t));
		in.read((char*) &cur, sizeof(PIXEL));
		if (occ)
		{
			for (j = 0; j < occ; j++)
			{
				data.push_back(cur);
				total += sizeof(PIXEL);
			}
		}
	}

	in.close();

	// Updating header informations
	image->imageSize = total;
	image->size = image->startOffset + image->imageSize;
	image->compression = 0x0000;

	// Writing the file
	std::fstream out;
	out.open(out_file, std::ios::out | std::ios::binary);

	out.write((char*) image, sizeof(_bitmap));

	for (const auto& item : data)
	{
		out.write((char*) &item, sizeof(PIXEL));
	}

	out.close();

	free(image);

	return EXIT_SUCCESS;
}
*/

__RLE_END__
