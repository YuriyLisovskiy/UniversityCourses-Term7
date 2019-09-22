#include <string>
#include <sys/stat.h>

#include "src/compression/rle.h"

const std::string IMAGES = "../../images/";
const std::string OUTPUT = "../../output/";

void prepare()
{
	const char* output_folder = "../../output";
	if (mkdir(output_folder, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH) == -1)
	{
		if (errno != EEXIST)
		{
			std::cout << "Can not create " << output_folder << " error: " << errno << std::endl;
			exit(-1);
		}
	}
}

void bmp_task()
{
	std::string base_file_name = "images_5";

	TimingData compress_td;
	rle::bmp_compress(
		(IMAGES + base_file_name + ".bmp"),
		(OUTPUT + base_file_name + "_compressed.bmp"),
		compress_td
	);
	std::cout << "Compressing:\n  reading: " << compress_td.reading_time << " ms\n  writing: " << compress_td.writing_time <<
		" ms\n  encoding: " << compress_td.encoding_time << " ms\n\n";

	TimingData decompress_td;
	rle::bmp_decompress(
		(OUTPUT + base_file_name + "_compressed.bmp"),
		(OUTPUT + base_file_name + "_uncompressed.bmp"),
		decompress_td
	);
	std::cout << "Decompressing:\n  reading: " << decompress_td.reading_time << " ms\n  writing: " << decompress_td.writing_time <<
		" ms\n  decoding: " << decompress_td.decoding_time << " ms\n";
}

int main()
{
	prepare();

	bmp_task();

	return 0;
}
