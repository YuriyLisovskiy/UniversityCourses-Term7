#include <string>
#include <sys/stat.h>

#include "src/compression/rle.h"

const std::string IMAGES = "../images/";
const std::string OUTPUT = "../output/";

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
	std::string base_file_name = "compressed.bmp";

	rle::bmp_compress(
		(IMAGES + "un" + base_file_name),
		(OUTPUT + base_file_name)
	);

	rle::bmp_decompress(
		(OUTPUT + base_file_name),
		(OUTPUT + "un" + base_file_name)
	);
}

int main()
{
	prepare();

	bmp_task();

	return 0;
}
