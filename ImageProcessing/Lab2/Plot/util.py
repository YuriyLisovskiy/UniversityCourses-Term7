import os


FILE_NAME = 'image_histogram'

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/ImageProcessing/ImageProcessing/Output/'
PLOT_FILE = BASE + '{}.txt'.format(FILE_NAME)

kwargs = dict(alpha=0.5, bins=100, density=True, stacked=True)


def read_plot_data():
	with open(PLOT_FILE, 'r') as file:
		r = [x.split(',')[1] for x in file.readline().rstrip('\n').split(';')]
		g = [x.split(',')[1] for x in file.readline().rstrip('\n').split(';')]
		b = [x.split(',')[1] for x in file.readline().rstrip('\n').split(';')]
		return r, g, b
