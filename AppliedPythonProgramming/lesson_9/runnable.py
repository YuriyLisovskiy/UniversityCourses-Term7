
common_data = 'common_data.txt'

with open(common_data, 'r') as data:
	numbers = list(map(int, data.readline().rstrip('\n').split(',')))


numbers = list(map(lambda x: x * 2, numbers))
print('subprocess - step 1:\n', numbers)


with open(common_data, 'w') as data:
	data.write(','.join(list(map(str, numbers))))
	data.write('\n')
