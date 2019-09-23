
def calc_y(pixel):
	return 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]


def calc_cb(pixel):
	return -0.1687 * pixel[0] - 0.3313 * pixel[1] - 0.5 * pixel[2] + 128


def calc_cr(pixel):
	return 0.5 * pixel[0] - 0.4187 * pixel[1] - 0.0813 * pixel[2] + 128


def rgb_to_ycbcr(pixels):
	result = []
	for row in pixels:
		new_row = []
		for pixel in row:
			new_row.append(
				[calc_y(pixel), calc_cb(pixel), calc_cr(pixel)]
			)
		result.append(new_row)
	return result


# Discrete cos transformation
def dct(ycbcr_pixels):
	# TODO
	pass


def jpeg_compress(pixels):
	# TODO
	pass


def jpeg_decompress(pixels):
	# TODO
	pass
