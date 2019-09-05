#include <string>
#include <sys/stat.h>

#include "src/compression/rle.h"

void prepare()
{
	const char* output_folder = "../output";
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
	std::string images = "../images/";
	std::string output = "../output/";
	std::string input_bmp_file_name = "uncompressed-24-bit.bmp";
	std::string output_bmp_file_name = "compressed.bmp";

	rle::bmp_compress(
		(images + input_bmp_file_name),
		(output + output_bmp_file_name)
	);

	rle::bmp_decompress(
		(output + output_bmp_file_name),
		(output + "un" + output_bmp_file_name)
	);
}

int main()
{
	prepare();

	bmp_task();

	return 0;
}
