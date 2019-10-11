import numpy as np
import matplotlib.image as mpimg


def im_hist(im):
	# calculates normalized histogram of an image
	m, n = im.shape
	h = [0.0] * 256
	for i in range(m):
		for j in range(n):
			h[im[i, j]] += 1
	return np.array(h)/(m*n)


def cum_sum(h):
	# finds cumulative sum of a numpy array, list
	return [sum(h[:i+1]) for i in range(len(h))]


def histeq(im):
	# calculate Histogram
	h = im_hist(im)
	cdf = np.array(cum_sum(h))  # cumulative distribution function
	sk = np.uint8(255 * cdf)    # finding transfer function values
	s1, s2 = im.shape
	Y = np.zeros_like(im)
	# applying transfered values for each pixels
	for i in range(0, s1):
		for j in range(0, s2):
			Y[i, j] = sk[im[i, j]]
	H = im_hist(Y)
	# return transformed image, original and new istogram,
	# and transform function
	return Y, h, H, sk


def equalize_img(img_in, img_out):
	img = np.uint8(mpimg.imread(img_in) * 255.0)
	# convert to grayscale
	# do for individual channels R, G, B, A for non-grayscale images

	img = np.uint8((0.2126 * img[:, :, 0]) + np.uint8(0.7152 * img[:, :, 1]) + np.uint8(0.0722 * img[:, :, 2]))

	new_img, h, new_h, sk = histeq(img)

	mpimg.imsave(img_out, new_img)
