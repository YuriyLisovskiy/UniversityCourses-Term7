import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Sobel's filters
sobel_horizontal = np.array([
	[-1, 0, 1],
	[-2, 0, 2],
	[-1, 0, 1]
])
sobel_vertical = np.array([
	[-1, -2, -1],
	[0, 0, 0],
	[1, 2, 1]
])

# Prewitt's filters
prewitt_horizontal = np.array([
	[-1, 0, 1],
	[-1, 0, 1],
	[-1, 0, 1]
])
prewitt_vertical = np.array([
	[-1, -1, -1],
	[0, 0, 0],
	[1, 1, 1]
])


def multiply_3x3(_filter, _img, i, j, chan):
	return (_filter[0, 0] * _img[i - 1, j - 1, chan]) + \
		(_filter[0, 1] * _img[i - 1, j, chan]) + \
		(_filter[0, 2] * _img[i - 1, j + 1, chan]) + \
		(_filter[1, 0] * _img[i, j - 1, chan]) + \
		(_filter[1, 1] * _img[i, j, chan]) + \
		(_filter[1, 2] * _img[i, j + 1, chan]) + \
		(_filter[2, 0] * _img[i + 1, j - 1, chan]) + \
		(_filter[2, 1] * _img[i + 1, j, chan]) + \
		(_filter[2, 2] * _img[i + 1, j + 1, chan])


def multiply_3x3_(_filter, _img, i, j, chan):
	y = np.array([
		[_img[i - 1, j - 1, chan], _img[i - 1, j, chan], _img[i - 1, j + 1, chan]],
		[_img[i, j - 1, chan], _img[i, j, chan], _img[i, j + 1, chan]],
		[_img[i + 1, j - 1, chan], _img[i + 1, j, chan], _img[i + 1, j + 1, chan]]
	])
	return _filter.dot(y)


def process(img_path, x_filter, y_filter):
	img = np.array(Image.open(img_path)).astype(np.uint8)
	h, w, d = img.shape

	gradient_image = np.zeros((h, w, d))

	multiply = multiply_3x3

	# offset by 1
	for channel in range(d):
		for i in range(1, h - 1):
			for j in range(1, w - 1):
				horizontal_grad = multiply(x_filter, img, i, j, channel)
				vertical_grad = multiply(y_filter, img, i, j, channel)

				# Edge Magnitude
				magnitude = np.sqrt(pow(horizontal_grad, 2.0) + pow(vertical_grad, 2.0))
				# Avoid underflow: clip result
				gradient_image[i - 1, j - 1, channel] = magnitude

	return gradient_image[:, :, 0] + gradient_image[:, :, 1] + gradient_image[:, :, 2]


def show(img):
	plt.figure()
	plt.imshow(img, cmap='gray')
	plt.show()
