from tifffile import tifffile as tiff
from tifffile import TiffFile
import numpy as np

from lzw import lzw


def tiff_compress():
	root = '~/Projects/UniversityCourses-Term7/ImageProcAndMult/'

	input_file = root + 'images/uncompressed.tiff'
	output_file = root + 'output/compressed.tiff'

	with TiffFile(input_file) as tif_file:
		uncompressed = np.array(tif_file.asarray()).flatten()

		compressed = lzw.compress(uncompressed.tolist())

		print(len(compressed))

		tiff.imsave(output_file, np.array(compressed))


def tiff_decompress():
	root = '~/Projects/UniversityCourses-Term7/ImageProcAndMult/'

	input_file = root + 'output/compressed.tiff'
	output_file = root + 'output/uncompressed.tiff'

	with TiffFile(input_file) as tif_file:
		compressed = np.array(tif_file.asarray()).flatten()

		decompressed = np.array(lzw.decompress(compressed.tolist()))

		tiff.imsave(output_file, decompressed.reshape((1200, 1200, 3)))


def main():
	# print(lzw.compress('hello,worlddddddd'))

	# tiff_compress()

	tiff_decompress()


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
