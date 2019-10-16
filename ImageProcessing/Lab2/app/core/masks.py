import numpy as np

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
