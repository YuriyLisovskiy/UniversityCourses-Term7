import numpy as np
import matplotlib.image as mp_img

from datetime import datetime

from app.core import masks


def calc_rgb_hist(img, opt):
	channel = {
		'r': img[:, :, 0],
		'g': img[:, :, 1],
		'b': img[:, :, 2]
	}[opt].astype('int')
	m, n, _ = img.shape
	hist = [0] * 256
	for i in range(m):
		for j in range(n):
			hist[channel[i, j]] += 1
	return np.array(hist)# / (m * n)


def calc_hsv_hist(image, opt):
	channel = {'h': 0, 's': 1, 'v': 2}[opt]
	m, n, _ = image.shape
	hs = [0] * 256
	for k in range(m):
		for l in range(n):
			hs[int(image[k, l, channel])] += 1
	return np.array(hs)


def calc_avg_hist(img):
	m, n, _ = img.shape
	hist = [0] * 256
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
	return np.array(hist)


def rgb2gray(image):
	return np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])


def equalize_gray_scale(img):
	def get_hist(image):
		m, n = image.shape
		hs = [0.0] * 256
		for k in range(m):
			for l in range(n):
				hs[int(img[k, l])] += 1
		return np.array(hs)

	hist = get_hist(img)
	colors_n = len(hist)
	h, w = img.shape
	num_of_pxs = h * w
	equalized = [0.0] * colors_n
	count = 0
	for i in range(colors_n):
		count += hist[i]
		mean = count / num_of_pxs
		equalized[i] = round(mean * (colors_n - 1))
	new_img = np.zeros_like(img)
	for x in range(h):
		for y in range(w):
			new_img[x, y] = equalized[int(img[x, y])]
	return new_img


def px_rgb2hsv(px):
	r, g, b = px
	max_, min_ = max(r, g, b), min(r, g, b)
	delta = max_ - min_

	# Value (Brightness)
	v = max_

	# Saturation
	s = delta / max_

	if min_ == max_:
		return 0.0, 0.0, v

	# Hue
	rc = (max_ - r) / delta
	gc = (max_ - g) / delta
	bc = (max_ - b) / delta
	if r == max_:
		h = bc - gc
	elif g == max_:
		h = 2.0 + rc - bc
	else:
		h = 4.0 + gc - rc
	h = (h / 6.0) % 1.0

	return h, s, v


def px_hsv2rgb(px):
	h, s, v = px
	if s == 0.0:
		return v, v, v

	k = int(h * 6.0)
	f = (h * 6.0) - k
	p = v * (1.0 - s)
	q = v * (1.0 - s * f)
	t = v * (1.0 - s * (1.0 - f))
	k %= 6
	if k == 0:
		return v, t, p
	if k == 1:
		return q, v, p
	if k == 2:
		return p, v, t
	if k == 3:
		return p, q, v
	if k == 4:
		return t, p, v
	if k == 5:
		return v, p, q

	raise ValueError('unable to calculate hsv pixel')


def rgb2hsv(img):
	hsi_image = np.zeros_like(img).astype('float')
	if len(img.shape) == 3:
		height, width, _ = img.shape
	else:
		height, width = img.shape
	for x in range(height):
		for y in range(width):
			hsi_image[x, y] = px_rgb2hsv(img[x, y])
	return hsi_image


def hsv2rgb(img):
	rgb_image = np.zeros_like(img).astype(np.uint8)
	if len(img.shape) == 3:
		height, width, _ = img.shape
	else:
		height, width = img.shape
	for x in range(height):
		for y in range(width):
			rgb_image[x, y] = px_hsv2rgb(img[x, y])
	return rgb_image


def equalize_hsv(img):
	now = datetime.now()

	colors_n = 256
	h, w, _ = img.shape
	num_of_pxs = h * w
	equalized = [0.0] * colors_n
	hist = calc_hsv_hist(img, 'v')
	cumulative_sum = 0
	for i in range(len(hist)):
		cumulative_sum += hist[i]
		mean = cumulative_sum / num_of_pxs
		equalized[i] = round(mean * (colors_n - 1))
	new_img = np.zeros_like(img)
	for x in range(h):
		for y in range(w):
			new_px = list(img[x, y])
			new_px[2] = equalized[int(img[x, y, 2])]
			new_img[x, y] = new_px

	print('HSV: {}'.format((datetime.now() - now).total_seconds()))

	return new_img


def equalize_rgb(img):
	now = datetime.now()

	colors_n = 256
	h, w, _ = img.shape
	num_of_pxs = h * w
	equalized = [0.0] * colors_n
	hist = calc_avg_hist(img)
	count = 0
	for i in range(len(hist)):
		count += hist[i]
		mean = count / num_of_pxs
		equalized[i] = round(mean * (colors_n - 1))
	new_img = np.zeros_like(img)
	for x in range(h):
		for y in range(w):
			new_img[x, y, 0] = equalized[img[x, y, 0]]
			new_img[x, y, 1] = equalized[img[x, y, 1]]
			new_img[x, y, 2] = equalized[img[x, y, 2]]

	print('RGB: {}'.format((datetime.now() - now).total_seconds()))

	return new_img


def equalize(img):
	px = img[0, 0]
	if px[0] == px[1] == px[2]:
		return equalize_gray_scale(rgb2gray(img))
	elif len(img.shape) == 3:
		if any([isinstance(chan, float) for chan in list(px)]):
			return equalize_hsv(img)
		elif all([isinstance(chan, int) or isinstance(chan, np.uint8) for chan in list(px)]):
			return equalize_rgb(img)
	else:
		raise AttributeError('images with shape "{}" are not supported'.format(len(img.shape)))


def calc_grad(_filter, _img, i, j, chan):
	if len(_filter) == 2:
		_img_part = np.array([
			[_img[i, j, chan], _img[i, j + 1, chan]],
			[_img[i + 1, j, chan], _img[i + 1, j + 1, chan]],
		])
	elif len(_filter) == 3:
		_img_part = np.array([
			[_img[i - 1, j - 1, chan], _img[i - 1, j, chan], _img[i - 1, j + 1, chan]],
			[_img[i, j - 1, chan], _img[i, j, chan], _img[i, j + 1, chan]],
			[_img[i + 1, j - 1, chan], _img[i + 1, j, chan], _img[i + 1, j + 1, chan]],
		])
	else:
		raise ValueError('filter is not supported')
	res = 0
	n = len(_filter)
	for i in range(n):
		for j in range(n):
			res += _filter[i, j] * _img_part[i, j]

	return res


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
	start = len(x_filter) - 2
	for channel in range(d):
		for i in range(start, h - 1):
			for j in range(start, w - 1):
				horizontal_grad = calc_grad(x_filter, img, i, j, channel)
				vertical_grad = calc_grad(y_filter, img, i, j, channel)

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


# Quick test region
if __name__ == '__main__':
	pass


"""
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
	h, s, i = float(px[0]), float(px[1]), float(px[2]) * 255
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
	if len(image.shape) == 3:
		height, width, _ = image.shape
	else:
		height, width = image.shape
	for x in range(height):
		for y in range(width):
			px = rgb2hsi_px(image[x, y])
			hsi_image[x, y] = px
	return hsi_image


def hsi2rgb(image):
	rgb_image = np.zeros_like(image).astype(np.uint8)
	if len(image.shape) == 3:
		height, width, _ = image.shape
	else:
		height, width = image.shape
	for x in range(height):
		for y in range(width):
			px = hsi2rgb_px(image[x, y])
			rgb_image[x, y] = px
	return rgb_image


def equalize_hsi(img):
	eps = 0.00000000001
	h, w, _ = img.shape
	num_of_pxs = h * w
	mean = 0.0
	new_img = np.array(img)
	while not abs(mean - 0.5) < eps:
		print(mean)
		for i in range(h):
			for j in range(w):
				mean += new_img[i, j, 2]
		mean /= num_of_pxs
		if mean != 0.5:
			theta = math.log(0.5, math.e) / math.log(mean, math.e)
			for x in range(h):
				for y in range(w):
					px = list(new_img[x, y])
					px[2] = (px[2] ** theta)
					new_img[x, y] = px

	# Checking hue and saturation
	# for x in range(h):
	# 	for y in range(w):
	# 		assert img[x, y, 0] == new_img[x, y, 0]
	# 		assert img[x, y, 1] == new_img[x, y, 1]

	return new_img


def equalize_hsi2(img):
	def calc_hsi_hist(image, opt):
		channel = {'h': 0, 's': 1, 'i': 2}[opt]
		m, n, _ = image.shape
		hs = [0.0] * 256
		for k in range(m):
			for l in range(n):
				hs[int(image[k, l, channel] * 255)] += 1
		return hs

	colors_n = 256
	h, w, _ = img.shape
	num_of_pxs = h * w
	equalized = [0.0] * colors_n
	hist = calc_hsi_hist(img, 'i')
	count = 0
	for i in range(len(hist)):
		count += hist[i]
		mean = count / num_of_pxs
		equalized[i] = round(mean * (colors_n - 1))
	new_img = np.zeros_like(img)
	for x in range(h):
		for y in range(w):
			new_px = list(img[x, y])
			new_px[2] = equalized[int(img[x, y, 2] * 255)]
			new_img[x, y] = new_px
	return new_img
"""
