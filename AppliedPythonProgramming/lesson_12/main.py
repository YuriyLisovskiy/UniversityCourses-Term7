"""
import os
import sys
import glob
import json
import time
from pprint import pprint
from datetime import datetime
from urllib.request import urlopen

dirname = 'data/'

remote_addr = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange/?mode=json'


def request(directory):
	filename = 'bank-exc-' + str(datetime.today().day) + '-' + str(datetime.today().month) + '.json'
	main_dir_name = os.path.abspath('.')
	dest_file = os.path.join(main_dir_name, directory, filename)
	try:
		remote_file = urlopen(remote_addr)
		with open(dest_file, 'w') as f_save:
			f_save.write(remote_file.read().decode('utf-8'))
		remote_file.close()
		reply = (True, dest_file)
	except Exception as _:
		info = sys.exc_info()
		reply = (False, info[0], info[1])
	return reply


def check_today_file():
	part = glob.glob(os.path.join(dirname, '*.json'))
	part.sort(key=os.path.getmtime, reverse=True)
	
	print('Available json files:')
	print(*[os.path.split(filename)[1] for filename in part], sep='\n')
	
	sttm = time.localtime(os.path.getmtime(part[0]))
	dmy = str(sttm.tm_mday) + '.' + str(sttm.tm_mon) + '.' + str(sttm.tm_year)
	print()
	
	if datetime.today() == dmy:
		return True, datetime.today(), os.path.split(part[0])[1]
	else:
		return False, dmy, os.path.split(part[0])[1]


def get_exchange_if_not_exists():
	if not check_today_file()[0]:
		print('... request ...')
		answer = request(dirname)
		print(answer)
		if not answer[0]:
			print('...pause...')
			time.sleep(3)
			print('... request repeat ...')
			answer2 = request(dirname)
			print(answer2)
		print('... finish')


def load_files_task():
	file_1 = 'bank-exc-25-11.json'
	file_2 = 'bank-exc-2-12.json'
	json_file_1 = os.path.join(dirname, file_1)
	json_file_2 = os.path.join(dirname, file_2)
	
	with open(json_file_1) as data_file:
		data_0212 = json.load(data_file)
	
	with open(json_file_2) as data_file:
		data_2511 = json.load(data_file)
	
	pprint(data_0212)
	pprint(data_2511)
"""

import os
import json
import time
from pprint import pprint
from datetime import datetime

files_dir = 'data/'


def get_data(p='bank-exc-2-12.json'):
	file_1 = p
	json_file_1 = os.path.join(files_dir, file_1)
	
	with open(json_file_1) as data_file:
		data_0212 = json.load(data_file)
	
	# pprint(data_0212)
	
	return data_0212


def task_close_to_uah_0_5():
	data_0212 = get_data()
	
	list_data = []
	
	data = data_0212[:]
	data.sort(key=lambda r: r['rate'], reverse=True)
	
	list_data.append('{0:^45}'.format('КУРСИ ЩОДО ГРИВНІ (+-)0.5'))
	list_data.append('-' * 54)
	list_data.append('| {0:<29}| {1:<9}| {2:<9}|'.format('Назва валюти', 'Курс', 'Різниця'))
	list_data.append('-' * 54)
	
	for k in range(len(data)):
		if abs(data[k]['rate'] - 1.0) <= 0.5:
			list_data.append(
				'| {0:<29}| {1:<9}| {2:<+9}|'.format(
					data[k]['txt'], round(data[k]['rate'], 2), round(data[k]['rate'] - 1.0, 2)
				)
			)
	list_data.append('-' * 54)
	for i in range(len(list_data)):
		print(list_data[i])
	
	report = 'report_close_to_uah_0_5.txt'
	file_report = os.path.join(files_dir, report)
	
	with open(file_report, 'w') as f:
		for line in list_data:
			f.write(line + '\n')


def _10_currencies_task(reverse=True):
	data_0212 = get_data()
	
	list_data = []
	
	today = str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(datetime.today().year)
	
	list_data.append('Звіт за {}'.format(today))
	
	data = data_0212[:]
	data.sort(key=lambda r: r['rate'], reverse=reverse)
	
	list_data.append('{0:^46}'.format('10 {} ОБМІННИХ КУРСІВ'.format('НАЙВИЩИХ' if reverse else 'НАЙНИЖЧИХ')))
	list_data.append('-' * 55)
	list_data.append('| {0:<34}| {1:<11}|'.format('Назва валюти', 'Курс обміну за 1'))
	list_data.append('-' * 55)
	
	for k in range(10):
		list_data.append('| {0:<34}| {1:<11}грн. |'.format(data[k]['txt'], data[k]['rate']))
	
	list_data.append('-' * 55)
	
	for i in range(len(list_data)):
		print(list_data[i])
	
	report = 'report_{}.txt'.format('top' if reverse else 'bottom')
	file_report = os.path.join(files_dir, report)
	
	with open(file_report, 'w') as f:
		for line in list_data:
			f.write(line + '\n')


def dynamic_analysis():
	json_file_1 = os.path.join(files_dir, 'bank-exc-2-12.json')
	json_file_2 = os.path.join(files_dir, 'bank-exc-25-11.json')
	
	with open(json_file_1) as data_file:
		data_0212 = json.load(data_file)
		
	with open(json_file_2) as data_file:
		data_2511 = json.load(data_file)
	
	sttm_1 = time.localtime(os.path.getmtime(json_file_1))
	dmy_1 = '{}.{}.{}'.format(
		sttm_1.tm_mday,
		sttm_1.tm_mon,
		sttm_1.tm_year
	)
	
	sttm_2 = time.localtime(os.path.getmtime(json_file_2))
	dmy_2 = '{}.{}.{}'.format(
		sttm_2.tm_mday,
		sttm_2.tm_mon,
		sttm_2.tm_year
	)
	
	list_data = []
	today = str(datetime.today().day) + '.' + str(datetime.today().month) + '.' + str(datetime.today().year)
	list_data.append('Звіт за {}'.format(today))
	
	def find_rate_exc(dt, code):
		i = -1
		for k in range(len(dt)):
			if dt[k]['r030'] == code:
				return dt[i]
		return None

	list_data.append(' {0:<28}| {1:<12}| {2:<12}| {3:<10}'.format(
		'Назва валюти', dmy_2, dmy_1, 'Різниця'
	))
	list_data.append('-' * 67)
	
	for currency in [840, 978, 124, 756, 826, 985]:
		fr_1 = find_rate_exc(data_2511, currency)
		fr_2 = find_rate_exc(data_0212, currency)
		if fr_1 and fr_2:
			list_data.append(' {0:<28}| {1:<12}| {2:<12}| {3:<+10}'.format(
				fr_1['txt'],
				round(fr_1['rate'], 2),
				round(fr_2['rate'], 2),
				round(fr_2['rate'] - fr_1['rate'], 2)
			))
	list_data.append('-' * 67)
	
	for i in range(len(list_data)):
		print(list_data[i])
	
	report = 'report_main.txt'
	file_report = os.path.join(files_dir, report)
	with open(file_report, 'w') as f:
		for line in list_data:
			f.write(line + '\n')
	

if __name__ == '__main__':
	# _10_currencies_task()
	# _10_currencies_task(False)
	dynamic_analysis()
