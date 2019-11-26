import os
import json
import subprocess
from pprint import pprint
from urllib import request

file_path = os.path.join(os.path.abspath('.'), 'data/test.json')


def task_1():
	parprog = subprocess.Popen(['gedit', file_path])


def print_json_file(path_to_file):
	with open(path_to_file) as f:
		data = json.load(f)
	pprint(data)


def task_3():
	addr = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange/?mode=json'
	file = 'data/bank-exc.json'
	response = request.urlopen(addr)
	with open(file, 'w') as f_save:
		f_save.write(response.read().decode(encoding='utf-8'))
	response.close()

	print_json_file(file)


def task_4():
	with open(file_path) as data_file:
		data = json.load(data_file)

	print('Тип цілого документа:', type(data).__name__)
	print('Документ має', len(data), 'елементів')
	print('Тип кожного елемента як цілого:', *[type(ob).__name__ for ob in data])
	print('\nТипи значень окремих елементів документа за ключами:', *[type(data[ob]).__name__ for ob in data.keys()])
	print('\nТип елемента \'chair\':', type(data['chair']).__name__)
	print('\nЗначення цілого елемента \'chair\':\n', data['chair'])
	print('\nПоелементний перелік частин \'chair\':')
	print(*[subvalue for subvalue in data['chair']], sep='\n')
	print(*[subvalue for subvalue in data['chair'].items()], sep='\n')
	print(
		'\nСписок значень окремих елементів документа:',
		*[str(ob) + ' : ' + str(data[ob]) for ob in data.keys()],
		sep='\n\n'
	)


def task_5():
	with open(file_path) as data_file:
		data = json.load(data_file)

	key1 = data.keys()
	# print(list(key1))
	for k in key1:
		if isinstance(data[k], dict):
			key2 = data[k].keys()
			# print(list(key2))
			if 'name' in key2 and 'price' in key2:
				# print('+')
				print('{0:10}{1}'.format(data[k]['name'], data[k]['price']))


if __name__ == '__main__':
	task_5()
