from PIL import Image

from rle import rle

IMAGES_ROOT = 'set_in_local_settings'
OUTPUT_ROOT = 'set_in_local_settings'

try:
	from local_settings import IMAGES_ROOT, OUTPUT_ROOT
except ImportError as e:
	raise e

IMAGE_NAME = 'images_5'


def bmp_compression():
	input_img = '{}{}.bmp'.format(IMAGES_ROOT, IMAGE_NAME)
	output_img = '{}compressed_{}.bmp'.format(OUTPUT_ROOT, IMAGE_NAME)

	img = Image.open(input_img)
	pixels = img.load()

	result_image = rle.bmp_compress(pixels)
	result_image.save(output_img, 'BMP')


def bmp_decompression():
	input_img = '{}compressed_{}.bmp'.format(OUTPUT_ROOT, IMAGE_NAME)
	output_img = '{}decompressed_{}.bmp'.format(OUTPUT_ROOT, IMAGE_NAME)

	img = Image.open(input_img)
	pixels = img.load()

	result_image = rle.bmp_decompress(pixels)
	result_image.save(output_img, 'BMP')


def main():
	bmp_compression()


if __name__ == '__main__':
	main()
