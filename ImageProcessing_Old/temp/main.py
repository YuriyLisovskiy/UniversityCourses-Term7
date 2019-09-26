import os
from datetime import datetime


if __name__ == '__main__':

	start = datetime.now()
	os.system('magick convert ../images/images_5.bmp -colors 256 -compress RLE ../output/images_5_8bit_rle.bmp')
	print('8-bit RLE:', (datetime.now() - start).total_seconds() * 1000)

	start = datetime.now()
	os.system('magick convert ../images/images_5.bmp -compress RLE ../output/images_5_rle.bmp')
	print('24-bit RLE:', (datetime.now() - start).total_seconds() * 1000)

	start = datetime.now()
	os.system('magick convert ../images/images_5.bmp -compress LZW ../output/images_5_lzw.tiff')
	print('LZW:', (datetime.now() - start).total_seconds() * 1000)

	start = datetime.now()
	os.system('magick convert ../images/images_5.bmp -compress JPEG ../output/images_5_se.jpeg')
	print('JPEG:', (datetime.now() - start).total_seconds() * 1000)
