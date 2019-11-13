import os
import subprocess


common_data = 'common_data.txt'
numbers = [4, 5, 6, 0, -1, -2, -3]

print('main process - step 1:\n', numbers)

with open(common_data, 'w') as data:
	data.write(','.join(list(map(str, numbers))))
	data.write('\n')

filename = os.path.join(os.path.abspath('.'), 'runnable.py')

subprocess.run(['python', filename])

with open(common_data, 'r') as data:
	numbers = list(map(int, data.readline().rstrip('\n').split(',')))

	print('main process - step 2:\n', list(map(lambda x: x + 1, numbers)))
