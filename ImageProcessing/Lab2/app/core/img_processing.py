import math
import numpy as np
import matplotlib.image as mp_img

from app.core import masks


def calc_hist(img, opt):
	channel = {
		'r': img[:, :, 0],
		'g': img[:, :, 1],
		'b': img[:, :, 2]
	}[opt].astype('int')
	m, n, _ = img.shape
	hist = [0.0] * 256
	for i in range(m):
		for j in range(n):
			hist[channel[i, j]] += 1
	return np.array(hist) / (m * n)


def calc_hist_hsi(img, opt):
	channel = {
		'h': 0,
		's': 1,
		'i': 2,
	}[opt]
	m, n, _ = img.shape
	hist = [0.0] * 256
	for i in range(m):
		for j in range(n):
			hist[int(img[i, j, channel] * 255)] += 1
	return hist


def calc_avg_hist(img):
	m, n, _ = img.shape
	hist = [0.0] * 256
	r_chan = img[:, :, 0]
	g_chan = img[:, :, 1]
	b_chan = img[:, :, 2]
	for x in range(m):
		for y in range(n):
			hist[r_chan[x, y]] += 1
			hist[g_chan[x, y]] += 1
			hist[b_chan[x, y]] += 1
	for i in range(256):
		hist[i] /= 3
	return hist


def rgb2hsi_px(px):
	eps = 0.00000001

	r, g, b = float(px[0]) / 255, float(px[1]) / 255, float(px[2]) / 255

	# Hue component
	numerator = 0.5 * ((r - g) + (r - b))
	denominator = math.sqrt((r - g) ** 2 + (r - b) * (g - b))
	theta = math.acos(numerator / (denominator + eps))
	h = theta
	if b > g:
		h = 2 * math.pi - h

	# Saturation component
	num = min(r, g, b)
	den = r + g + b
	if den == 0:
		den = eps
	s = 1 - 3 * num / den
	if s == 0:
		h = 0

	# Intensity component
	i = (r + g + b) / 3

	return h, s, i


def hsi2rgb_px(px):
	h, s, i = float(px[0]), float(px[1]), float(px[2])
	if 0 <= h < 2 * math.pi / 3:
		b = i * (1 - s)
		r = i * (1 + (s * math.cos(h)) / math.cos(math.pi / 3 - h))
		g = 3 * i - (r + b)
	elif 2 * math.pi / 3 <= h < 4 * math.pi / 3:
		r = i * (1 - s)
		g = i * (1 + (s * math.cos(h - 2 * math.pi / 3) / math.cos(math.pi / 3 - (h - 2 * math.pi / 3))))
		b = 3 * i - (r + g)
	elif 4 * math.pi / 3 <= h <= 2 * math.pi:
		g = i * (1 - s)
		b = i * (1 + (s * math.cos(h - 4 * math.pi / 3) / math.cos(math.pi / 3 - (h - 4 * math.pi / 3))))
		r = 3 * i - (g + b)
	else:
		raise IndexError('h is out of range: {}'.format(h))
	return round(r), round(g), round(b)


def rgb2hsi(image):
	hsi_image = np.zeros_like(image).astype('float')
	height, width, _ = image.shape
	for x in range(height):
		for y in range(width):
			px = rgb2hsi_px(image[x, y])
			hsi_image[x, y] = px
	return np.array(hsi_image)


def hsi2rgb(image):
	rgb_image = np.zeros_like(image).astype(np.uint8)
	height, width, _ = image.shape
	for x in range(height):
		for y in range(width):
			px = hsi2rgb_px(image[x, y])
			rgb_image[x, y] = px
	return np.array(rgb_image)


def equalize_hsi(img):
	_l = 256
	h, w, _ = img.shape
	num_of_pxs = h * w
	cdf = [0.0] * 256
	equalized = [0.0] * 256
	hist = calc_hist_hsi(img, 'i')
	count = 0
	for i in range(len(hist)):
		count += hist[i]
		cdf[i] = count / num_of_pxs
		equalized[i] = round(cdf[i] * (_l - 1))
	new_img = np.zeros_like(img)
	for x in range(h):
		for y in range(w):
			px = list(img[x, y])
			px[2] = equalized[int(px[2] * 255)]
			new_img[x, y] = px
	return new_img


def equalize_rgb(img):
	_l = 256
	h, w, _ = img.shape
	num_of_pxs = h * w
	cdf = [0.0] * 256
	equalized = [0.0] * 256
	hist = calc_avg_hist(img)
	count = 0
	for i in range(len(hist)):
		count += hist[i]
		cdf[i] = count / num_of_pxs
		equalized[i] = round(cdf[i] * (_l - 1))
	new_img = np.zeros_like(img)
	for x in range(h):
		for y in range(w):
			new_img[x, y, 0] = equalized[img[x, y, 0]]
			new_img[x, y, 1] = equalized[img[x, y, 1]]
			new_img[x, y, 2] = equalized[img[x, y, 2]]
	return new_img


def calc_grad_2x2(_filter, _img, i, j, chan):
	return (_filter[0, 0] * _img[i, j, chan]) + \
		(_filter[0, 1] * _img[i, j + 1, chan]) + \
		(_filter[1, 0] * _img[i + 1, j, chan]) + \
		(_filter[1, 1] * _img[i + 1, j + 1, chan])


def calc_grad_3x3(_filter, _img, i, j, chan):
	return (_filter[0, 0] * _img[i - 1, j - 1, chan]) + \
		(_filter[0, 1] * _img[i - 1, j, chan]) + \
		(_filter[0, 2] * _img[i - 1, j + 1, chan]) + \
		(_filter[1, 0] * _img[i, j - 1, chan]) + \
		(_filter[1, 1] * _img[i, j, chan]) + \
		(_filter[1, 2] * _img[i, j + 1, chan]) + \
		(_filter[2, 0] * _img[i + 1, j - 1, chan]) + \
		(_filter[2, 1] * _img[i + 1, j, chan]) + \
		(_filter[2, 2] * _img[i + 1, j + 1, chan])


def process_op(img, x_filter, y_filter):
	assert len(x_filter) == len(y_filter)
	h, w, d = img.shape
	gradient_image = np.zeros((h, w, d))
	multiply, start = {
		2: (calc_grad_2x2, 0),
		3: (calc_grad_3x3, 1)
	}[len(x_filter)]
	for channel in range(d):
		for i in range(start, h - 1):
			for j in range(start, w - 1):
				horizontal_grad = multiply(x_filter, img, i, j, channel)
				vertical_grad = multiply(y_filter, img, i, j, channel)

				magnitude = np.sqrt(pow(horizontal_grad, 2.0) + pow(vertical_grad, 2.0))
				gradient_image[i - 1, j - 1, channel] = magnitude

	return gradient_image[:, :, 0] + gradient_image[:, :, 1] + gradient_image[:, :, 2]


def sobel(img):
	return process_op(img, masks.sobel_horizontal, masks.sobel_vertical)


def prewitt(img):
	return process_op(img, masks.prewitt_horizontal, masks.prewitt_vertical)


def robert(img):
	return process_op(img, masks.robert_horizontal, masks.robert_vertical)


def save_gray(_path, img):
	mp_img.imsave(_path, img, cmap='gray')
