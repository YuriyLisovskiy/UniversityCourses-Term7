from PIL import Image

from jpeg import jpeg

IMAGES_ROOT = 'set_in_local_settings'
OUTPUT_ROOT = 'set_in_local_settings'

try:
	from local_settings import IMAGES_ROOT, OUTPUT_ROOT
except ImportError as e:
	raise e

IMAGE_NAME = 'images_5'


def jpeg_compression():
	input_img = '{}{}.bmp'.format(IMAGES_ROOT, IMAGE_NAME)
	output_img = '{}{}.jpg'.format(OUTPUT_ROOT, IMAGE_NAME)

	img = Image.open(input_img)
	pixels = img.load()

	result_image = jpeg.jpeg_compress(pixels)
	result_image.save(output_img, 'JPEG')


def jpeg_decompression():
	pass


def main():
	pass


if __name__ == '__main__':
	main()
