import numpy as np


def calc_hist(img, opt):
	channel = {
		'r': img[:, :, 0],
		'g': img[:, :, 1],
		'b': img[:, :, 2],
	}[opt]
	m, n, _ = img.shape
	hist = [0.0] * 256
	for i in range(m):
		for j in range(n):
			hist[channel[i, j]] += 1
	return np.array(hist) / (m * n)


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
