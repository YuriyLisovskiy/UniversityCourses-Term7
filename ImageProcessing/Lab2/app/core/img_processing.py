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
		'h': img[:, :, 0],
		's': img[:, :, 1],
		'i': img[:, :, 2],
	}[opt]
	m, n, _ = img.shape
	hist = {}
	for i in range(m):
		for j in range(n):
			color = channel[i, j]
			if color not in hist:
				hist[color] = 0
			hist[color] += 1
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
	_r, _g, _b = float(px[0]) / 255, float(px[1]) / 255, float(px[2]) / 255
	min_ = 1.e-6
	_i = _r + _g + _b
	if _i == 0:
		_i += 0.001
	_i /= 3
	r = _r / _i
	g = _g / _i
	b = _b / _i
	if _r == _g and _g == _b:
		_s = 0
		_h = 0
	else:
		w = 0.5 * (_r - _g + _r - _b) / math.sqrt((_r - _g) * (_r - _g) + (_r - _b) * (_g - _b))
		if w > 1:
			w = 1
		elif w < -1:
			w = -1
		_h = math.acos(w)
		if _h < 0:
			print('H < 0: {}'.format(_h))
		if _b > _g:
			_h = 2 * math.pi - _h
		_s = 1 - 3 * min(_r, _g, _b) / _i
	return _h, _s, _i


def hsi2rgb_px(px):
	h, s, i = float(px[0]), float(px[1]), float(px[2])
	if s > 1:
		s = 1
	if i > 1:
		i = 1
	if s == 0:
		r = g = b = i
	else:
		if 0 <= h < 2 * math.pi / 3:
			b = (1 - s) / 3
			r = (1 + s * math.cos(h) / math.cos(math.pi / 3 - h)) / 3
			g = 1 - r - b
		elif 2 * math.pi / 3 <= h < 4 * math.pi / 3:
			h -= 2 * math.pi / 3
			r = (1 - s) / 3
			g = (1 + s * math.cos(h) / math.cos(math.pi / 3 - h)) / 3
			b = 1 - r - g
		elif 4 * math.pi / 3 <= h < 2 * math.pi:
			h -= 4 * math.pi / 3
			g = (1 - s) / 3
			b = (1 + s * math.cos(h) / math.cos(math.pi / 3 - h)) / 3
			r = 1 - b - g
		else:
			raise IndexError('h out of range: {}'.format(h * 180 / math.pi))
		if r < 0 or g < 0 or b < 0:
			pass
			# print('r, g, b: {}, {}, {}\nh, s, i: {}, {}, {}'.format(r, g, b, h, s, i))
		if r < 0:
			r = 0
		if g < 0:
			g = 0
		if b < 0:
			b = 0
		r = 3 * i * r
		g = 3 * i * g
		b = 3 * i * b
		if r > 1:
			r = 1
		if g > 1:
			g = 1
		if b > 1:
			b = 1
	return int(r * 255), int(g * 255), int(b * 255)


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
	cdf = {}
	equalized = {}
	hist = calc_hist_hsi(img, 'i')
	count = 0
	for key, value in hist.items():
		count += value
		cdf[key] = count / num_of_pxs
		equalized[key] = round(cdf[key] * (_l - 1))
	new_img = np.zeros_like(img)
	for x in range(h):
		for y in range(w):
			hsv_px = (
				img[x, y, 0],
				img[x, y, 1],
				equalized[img[x, y, 2]]
			)
			new_img[x, y] = hsv_px
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
