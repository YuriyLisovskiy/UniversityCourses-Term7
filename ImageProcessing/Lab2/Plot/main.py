import os
import matplotlib.pyplot as plt


FILE_NAME = 'image_1_histogram'

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/ImageProcessing/ImageProcessing/Output/'
PLOT_FILE = BASE + '{}.txt'.format(FILE_NAME)

kwargs = dict(alpha=0.5, bins=100, density=True, stacked=True)


def read_plot_data(plot_file):
	with open(plot_file, 'r') as file:
		r = [x.split(',')[1] for x in file.readline().rstrip('\n').split(';')]
		g = [x.split(',')[1] for x in file.readline().rstrip('\n').split(';')]
		b = [x.split(',')[1] for x in file.readline().rstrip('\n').split(';')]
		return r, g, b


def main():
	r, g, b = read_plot_data(PLOT_FILE)
	plt.hist(r, **kwargs, color='r', label='Red channel')
	plt.hist(g, **kwargs, color='g', label='Green channel')
	plt.hist(b, **kwargs, color='b', label='Blue channel')
	plt.ylabel('Frequency')
	plt.xlabel('Pixel values [0;255]')
	plt.xlim(0, 255)
	plt.show()


if __name__ == '__main__':
	main()
