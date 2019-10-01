def fn(**kwargs):
	print(kwargs)


def main():
	fn(a=1, b=2)

# 	data = open('./data.txt', 'r')
# 	matrix = [
# 		sorted([(int(x), ) for x in file_row.rstrip('\n').split()]) for file_row in data
# 	]
# 	data.close()

# 	for r in matrix:
# 		print('min: {}, max: {}, row: {}'.format(r[0][0], r[-1][0], r[1]))

# 	_min = min([min(row) for row in matrix])
# 	_max = max([max(row) for row in matrix])

# 	print('\nMin: {}, Max: {}'.format(_min, _max))

# 	res_file = open('min_max_data.txt', 'w')
# 	res_file.write('Min: {}\n'.format(_min))
# 	res_file.write('Max: {}\n'.format(_max))
# 	res_file.close()


if __name__ == '__main__':
	main()
