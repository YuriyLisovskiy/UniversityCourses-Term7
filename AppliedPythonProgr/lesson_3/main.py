def _range(first, last, step=1):
	print('_range called')
	for k in range(first, last, step):
		yield k


def pretty(d, indent=0):
	for key, value in d.items():
		print('\t' * indent + str(key))
		if isinstance(value, dict):
			pretty(value, indent+1)
		else:
			print('\t' * (indent+1) + str(value))


if __name__ == '__main__':

	goods_list = 'сир,хліб,масло,помідори,перець,печиво,цукерки,олія,пиво'

	shop_1 = 'хліб,масло,олія,сир'
	shop_2 = 'цукерки,помідори,олія,пиво,сир,масло'
	shop_3 = 'батон'

	goods_set = {x for x in goods_list.split(',')}
	shop_1_set = {x for x in shop_1.split(',')}
	shop_2_set = {x for x in shop_2.split(',')}
	shop_3_set = {x for x in shop_3.split(',')}

	all_order = shop_1_set | shop_2_set | shop_3_set
	print('All orders:', all_order)

	not_ordered = goods_set - all_order
	print('Not ordered:', not_ordered)

	popular_order = shop_1_set & shop_2_set & shop_3_set
	print('The most popular:', popular_order)

	unable_to_sell = goods_set - all_order
	print('Unable to sell:', unable_to_sell)

"""
	sentence = 'гарна погода нікому не зашкодить.'
	a = set()
	b = set()

	for c in sentence.replace('.', '').replace(' ', ''):
		if c not in a:
			a.add(c)
		else:
			b.add(c)

	print(sorted(list(b)))
	print(sorted(list(a - b)))

	ukr_low = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'

	print(sorted(list(set(ukr_low) - a)))
"""

"""
	experiment = [8, 0, 9, 4, 4, 0, 0, 5, 4, 9, 8, 9]
	diff = list(set(experiment))
	diff.sort(reverse=True)
	print(diff)
"""

"""
	with open('tram_data.txt', 'r') as tram_data:
		result = []
		for line in tram_data.readlines():
			result.append(tuple(line.replace('\n', '').split(',')))
		
		print('Using dictionary:')
	
		data_dict = {int(x[0]): x[1].split('-') for x in result}
		limit_stops_dict = {key: (value[0], value[-1]) for key, value in data_dict.items()}
		for key, value in limit_stops_dict.items():
			print(key, ':', ' - '.join(value))
	
		print([key for key, value in data_dict.items() if 'вул. І. Франка' in value])
	
		print('\nUsing list:')
	
		data_list = [(int(x[0]), x[1].split('-')) for x in result]
		limit_stops_list = [(item[0], (item[1][0], item[1][-1])) for item in data_list]
		for item in limit_stops_list:
			print(item[0], ':', ' - '.join(item[1]))
	
		print([item[0] for item in data_list if 'вул. І. Франка' in item[1]])
"""
