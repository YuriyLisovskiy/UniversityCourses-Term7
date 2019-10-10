"""
from datetime import datetime
from functools import reduce

template = '''Магазин: {}
	Назва товару: {}
	Ціна: {}
	Дата: {}
'''


def bill(place, name, price, date):
	print(template.format(place, name, price, date))


def bill_tuple(*args):
	print(template.format(args[0], args[1], args[2], args[3]))


def bill_dict(**kwargs):
	print('''Магазин: {place}
	Назва товару: {name}
	Ціна: {price}
	Дата: {date}
'''.format(**kwargs))


# У файлі є товари
# Перевірити: чи кожна ціна є цілим числом, чи кожна ціна (x) є 10 < x < 100

# Прочитати файл
# Застосувати ф-цію map() при перевірці числа на ціле
# Застосувати ф-цію map() при перевірці 10 < x < 100
# Застос reduce, щоб вибрати ті, де є true


def task_2():

	def conv(s):
		try:
			return int(s)
		except ValueError:
			return float(s)

	with open('data.txt', 'r') as file:

		goods = [conv(x.rstrip('\n')) for x in file.readlines()]
		print(goods)

		print(list(map(lambda x: isinstance(x, int), goods)))

		print(list(map(lambda x: 10 < x < 100, goods)))
"""

import random


def task_1():
	n = 100

	nums = [random.randint(-50, 50) for _ in range(n)]

	print('Numbers:', nums)
	print('Max:', max(nums))
	print('Min:', min(nums))
	print('R:', max(nums) - min(nums))

	# nums.sort()

	print('Frequencies:', {x: nums.count(x) for x in nums})
	print('Not in list:', len(set([x for x in range(-50, 50)]) - set(nums)))


def is_prime(n):
	if n <= 1:
		return False
	if n <= 3:
		return True

	if n % 2 == 0 or n % 3 == 0:
		return False

	i = 5
	while i * i <= n:
		if n % i == 0 or n % (i + 2) == 0:
			return False
		i = i + 6

	return True


def is_palindrome(num):
	return num == int(''.join(reversed(str(num))))


def max_palindrome_prod_of_two_nums(arr):
	n = len(arr)
	if n < 2:
		return arr

	a = arr[0]
	b = arr[1]
	prod = a * b

	for i in range(0, n):
		for j in range(i + 1, n):
			if arr[i] * arr[j] > a * b and is_palindrome(arr[i] * arr[j]):
				a = arr[i]
				b = arr[j]
				prod = a * b

	return {a, b}, prod


def task_2():
	nums = [x for x in range(100, 1000)]
	primes = []
	for num in nums:
		if is_prime(num):
			primes.append(num)
	print(max_palindrome_prod_of_two_nums(primes))


def main():
	task_2()


if __name__ == '__main__':
	main()
