import numpy as np


def calc_hist(img):
	# calculates normalized histogram of an image
	m, n = img.shape
	h = [0.0] * 256
	for i in range(m):
		for j in range(n):
			h[img[i, j]] += 1
	return np.array(h) / (m * n)


def cumulative_sum(arr):
	return [sum(arr[:i+1]) for i in range(len(arr))]


def equalize(img):
	# calculate Histogram
	img_hist = calc_hist(img)
	cdf = np.array(cumulative_sum(img_hist))    # cumulative distribution function
	sk = np.uint8(255 * cdf)                    # finding transfer function values
	m, n = img.shape
	new_img = np.zeros_like(img)

	# applying transferred values for each pixels
	for i in range(m):
		for j in range(n):
			new_img[i, j] = sk[img[i, j]]
	new_img_hist = calc_hist(new_img)

	# return transformed image, original and new histogram,
	# and transform function
	return new_img, img_hist, new_img_hist, sk


def rgb_equalize(img):
	r = img[:, :, 0]
	g = img[:, :, 1]
	b = img[:, :, 2]

	r_eq, r_hist, r_eq_hist, _ = equalize(r)
	g_eq, g_hist, g_eq_hist, _ = equalize(g)
	b_eq, b_hist, b_eq_hist, _ = equalize(b)

	h, w, _ = img.shape
	img_out = np.zeros_like(img)

	img_out[:, :, 0] = r_eq
	img_out[:, :, 1] = g_eq
	img_out[:, :, 2] = b_eq

	return img_out, r_hist, g_hist, b_hist, r_eq_hist, g_eq_hist, b_eq_hist
