from PIL import Image


def compare(left, right):
	return left[0] == right[0] and left[1] == right[1] and left[2] == right[2]


def bmp_compress(width, height, matrix):
	pixels = []
	for i in range(len(matrix)):
		pixels += matrix[i]

	current = pixels.pop(0)

	repetition = 1
	result_pixels = []
	for _next in pixels:
		if not compare(current, _next):
			result_pixels.append((
				repetition,
				current[0],
				current[1],
				current[2]
			))
			repetition = 0
		repetition += 1
		current = _next
	if repetition > 1:
		result_pixels.append((
			repetition,
			current[0],
			current[1],
			current[2]
		))

	img = Image.new("RGB", (1, len(result_pixels)))
	pxs = img.load()
	for y in range(len(result_pixels)):
		pxs[0, y] = result_pixels[y]

	return img


def bmp_decompress(pixels):
	pass
