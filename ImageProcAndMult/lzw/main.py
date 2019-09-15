from tifffile import tifffile as tiff
from tifffile import TiffFile
import numpy as np

from lzw import lzw
from tracker.time_tracker import TimeTracker


IMAGES_ROOT = 'set_in_local_settings'
OUTPUT_ROOT = 'set_in_local_settings'

IMAGE_NAME = 'images_5'


try:
	from local_settings import IMAGES_ROOT, OUTPUT_ROOT
except ImportError as e:
	raise e


def tiff_compress():
	input_file = IMAGES_ROOT + '{}.tiff'.format(IMAGE_NAME)
	output_file = OUTPUT_ROOT + '{}_compressed.tiff'.format(IMAGE_NAME)

	t = TimeTracker()

	t.start('reading')
	tif_file = TiffFile(input_file)
	image_matrix = tif_file.asarray()
	t.track('reading')

	# print(image_matrix)

	t.start('compression')
	compressed = lzw.compress(image_matrix.flatten().tolist())
	t.track('compression')

	t.start('writing')
	tiff.imsave(output_file, np.array(compressed))
	t.track('writing')

	print(t)

	return image_matrix.shape


def tiff_decompress(dimensions):
	input_file = OUTPUT_ROOT + '{}_compressed.tiff'.format(IMAGE_NAME)
	output_file = OUTPUT_ROOT + '{}_uncompressed.tiff'.format(IMAGE_NAME)

	tif_file = TiffFile(input_file)
	compressed = np.array(tif_file.asarray()).flatten()
	decompressed = np.array(lzw.decompress(compressed.tolist()))

	# print(decompressed.reshape(dimensions))

	tiff.imwrite(output_file, decompressed.reshape(dimensions))


def test():
	to_compress = [241, 16, 72, 10, 10, 10, 10, 10, 241, 16, 72, 13, 5]

	compressed = lzw.compress(to_compress)
	print(compressed)

	decompressed = lzw.decompress(compressed)
	print(decompressed)


def main():

	dimensions = tiff_compress()
	print(dimensions)
	tiff_decompress(dimensions)

	# test()


if __name__ == '__main__':
	main()


"""

	# with TiffFile(input_file) as tif_file:

	# 	image = tif_file.asarray()

	# 	arr = np.array(image).flatten()

		# new_image = arr.reshape((1200, 1200, 3))

	# 	tiff.imsave(output_file, )

		# resolution = tif_file.pages[0].tags['XResolution']
		# print(resolution.value)

#	img = tiff.imread(input_file)

#	print(img[600])

#	tiff.imsave(output_file, img)

"""
