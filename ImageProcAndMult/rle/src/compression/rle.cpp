#include "rle.h"

__RLE_BEGIN__

#define READING "reading"
#define WRITING "writing"
#define ENCODING "encoding"
#define DECODING "decoding"

/*

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

	// Updating header information
	image->imageSize = total;
	image->size = image->startOffset + image->imageSize;
	image->compression = 4;

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

int bmp_decompress(const std::string& input_file, const std::string& out_file, TimingData& td)
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

	// Updating header information
	image->imageSize = total;
	image->size = image->startOffset + image->imageSize;
	image->compression = 0;

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

*/

const uint8_t lineFeed = 0x00;
const uint8_t imageEnd = 0x01;

int bmp_compress(const std::string& input_file, const std::string& out_file, TimingData& td)
{
	uint32_t i, total = 0;
	bool ok = true;
	uint8_t occ = 1, cur, cur2;
	bool readRef = true;
	std::fstream in, out;
	uint8_t* pallet;
	std::vector<uint8_t> data;

	// Reading the file
	auto* image = new _bitmap();

	in.open(input_file, std::ios::binary | std::ios::in);

	memset(image, 0x00, sizeof (_bitmap));
	in.read((char*) image, sizeof(_bitmap));

	// Controlling the magic number and the header size
	if (image->magicNumber[0] != 'B' || image->magicNumber[1] != 'M'
	    || image->headerSize != 40 || image->depth != 8
	    || image->compression)
	{
		fprintf(stderr, "Error: Incompatible file type\n");
		ok = false;
		goto cleaning;
	}

	// Controlling the start offset
	if (image->startOffset < sizeof (_bitmap))
	{
		fprintf(stderr, "Error: Wrong start offset\n");
		ok = false;
		goto cleaning;
	}

	// Skipping data from the beginning to the start offset
	pallet = (uint8_t*) malloc(image->startOffset - sizeof (_bitmap));
	if (!pallet)
	{
		fprintf(stderr, "Error while allocating memory\n");
		ok = false;
		goto cleaning;
	}

	for (i = 0; i < (image->startOffset - sizeof (_bitmap)) / FILE_BUFFER_SIZE; i++)
	{
		in.read((char*) (pallet + i * FILE_BUFFER_SIZE), FILE_BUFFER_SIZE);
	}

	in.read((char*) (pallet + i * FILE_BUFFER_SIZE), (image->startOffset - sizeof (_bitmap)) % FILE_BUFFER_SIZE);

	// RLE compression
	in.read((char*) &cur, sizeof(uint8_t));
	for (i = 0; i < image->imageSize; i++)
	{
		// End of line
		if (i && !(i % image->width))
		{
			if (occ)
			{
				data.push_back(occ);
				data.push_back(cur);
				total += 2;
			}

			data.push_back(0x00);
			data.push_back(lineFeed);
			total += 2;

			occ = 0;
			readRef = true;
		}

		// Max occurrences
		if (255 == occ)
		{
			data.push_back(occ);
			data.push_back(cur);
			total += 2;

			occ = 0;
			readRef = true;
		}

		if (readRef)
		{
			in.read((char*) &cur, sizeof(uint8_t));
			occ++;
			readRef = false;
		}
		else
		{
			in.read((char*) &cur2, sizeof(uint8_t));
			if (cur == cur2)
			{
				occ++;
			}
			else
			{
				data.push_back(occ);
				data.push_back(cur);
				total += 2;

				occ = 1;
				cur = cur2;
			}
		}
	}
	in.close();

	// End of the last line
	if (occ)
	{
		data.push_back(occ);
		data.push_back(cur);
		total += 2;
	}

	// End of the pic
	data.push_back(0x00);
	data.push_back(imageEnd);
	total += 2;

	fprintf(stdout, "Compression ratio = %f%%\n", 100.0 - (image->startOffset + total) * 100.0 / image->size);

	// Updating header information
	image->imageSize = total;
	image->size = image->startOffset + image->imageSize;
	image->compression = 0x0001;

	// Writing the file
	out.open(out_file, std::ios::binary | std::ios::out);

	out.write((char*) image, sizeof(_bitmap));
	out.write((char*) pallet, image->startOffset - sizeof (_bitmap));
	for (const auto& px : data)
	{
		out.write((char*) &px, total * sizeof(uint8_t));
	}

cleaning:
	if (image)
	{
		free(image);
	}

	if (pallet)
	{
		free(pallet);
	}

//	if (data)
//	{
//		free(data);
//	}

	if (in.is_open())
	{
		in.close();
	}

	if (out.is_open())
	{
		out.close();
	}

	if (!ok)
	{
		return EXIT_FAILURE;
	}
	else
	{
		return EXIT_SUCCESS;
	}
}

int bmp_decompress(const std::string& input_file, const std::string& out_file, TimingData& td)
{
	bool ok = true;
	uint32_t i, j, total = 0;
	uint8_t couples[2];
//	uint8_t* data;
	uint8_t* pallet;
	std::fstream in, out;
	std::vector<uint8_t> data;

	// Reading the file
	auto image = new _bitmap();
	memset(image, 0x00, sizeof (_bitmap));

	in.open(input_file, std::ios::binary | std::ios::in);

	in.read((char*) image, sizeof(_bitmap));

	// Controlling the magic number and the header size
	if (image->magicNumber[0] != 'B' || image->magicNumber[1] != 'M'
	    || image->headerSize != 40 || image->depth != 8
	    || image->compression != 1)
	{
		fprintf(stderr, "Error: Incompatible file type\n");
		ok = false;
		goto cleaning;
	}

	// Controlling the start offset
	if (image->startOffset < sizeof (_bitmap))
	{
		fprintf(stderr, "Error: Wrong start offset\n");
		ok = false;
		goto cleaning;
	}

	// Skipping data from the beginning to the start offset
	pallet = (uint8_t*) malloc(image->startOffset - sizeof(_bitmap));
	if (!pallet)
	{
		fprintf(stderr, "Error while allocating memory\n");
		ok = false;
		goto cleaning;
	}

	for (i = 0; i < (image->startOffset - sizeof (_bitmap)) / FILE_BUFFER_SIZE; i++)
	{
		in.read((char*) (pallet + i * FILE_BUFFER_SIZE), FILE_BUFFER_SIZE);
	}

	in.read((char*) (pallet + i * FILE_BUFFER_SIZE), (image->startOffset - sizeof (_bitmap)) % FILE_BUFFER_SIZE);

	// RLE decompression
	for (i = 0; i < image->imageSize / 2; i++)
	{
		in.read((char*) &couples, 2 * sizeof(uint8_t));
		if (couples[0])
		{
			for (j = 0; j < couples[0]; j++)
			{
				data.push_back(couples[1]);
				total++;
			}
		}
	}

	in.close();

	// Updating header information
	image->imageSize = total;
	image->size = image->startOffset + image->imageSize;
	image->compression = 0x0000;

	// Writing the file
	out.open(out_file, std::ios::binary | std::ios::out);

	out.write((char*) image, sizeof(_bitmap));
	out.write((char*) pallet, image->startOffset - sizeof (_bitmap));
	for (const auto& px : data)
	{
		out.write((char*) &px, sizeof(uint8_t));
	}

	out.close();

cleaning:
	if (image)
	{
		free(image);
	}

	if (pallet)
	{
		free(pallet);
	}

//	if (data)
//	{
//		free(data);
//	}

	if (in.is_open())
	{
		in.close();
	}

	if (out.is_open())
	{
		out.close();
	}

	if (!ok)
	{
		return EXIT_FAILURE;
	}
	else
	{
		return EXIT_SUCCESS;
	}
}

__RLE_END__
