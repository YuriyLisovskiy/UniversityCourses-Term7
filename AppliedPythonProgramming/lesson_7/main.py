
class DynArrError(Exception):
	pass


class DynArr:

	def __init__(self, obj=None, from_keys=True):
		self.arr = []
		if obj:
			if isinstance(obj, list) or isinstance(obj, tuple):
				self.arr = list(obj)[:]
			elif isinstance(obj, dict):
				if from_keys:
					self.arr = list(obj.keys())[:]
				else:
					self.arr = list(obj.values())[:]

	def __str__(self):
		return '[{}]'.format(', '.join(map(str, self.arr)))

	def set_val(self, num, val):
		if 0 <= num < len(self.arr):
			self.arr[num] = val
		else:
			raise DynArrError('index out of range: {}'.format(num))

	def get_val(self, num):
		if 0 <= num < len(self.arr):
			return self.arr[num]
		else:
			raise DynArrError()

	def insert(self, pos, obj, separate=True):
		if 0 > pos > len(self.arr) - 1:
			raise DynArrError('index out of range: {}'.format(pos))
		if separate and (isinstance(obj, list) or isinstance(obj, tuple)):
			self.arr[pos:pos] = list(obj)
		else:
			self.arr.insert(pos, obj)

	def delete(self, n_form, n_to):
		del self.arr[n_form:n_to]


class Trip:

	def __init__(self):
		self.places = []

	def __str__(self):
		return ', '.join([self.go_back() for _ in range(len(self.places))])

	def __bool__(self):
		return bool(self.places)

	def visit(self, place):
		self.places.append(place)

	def go_back(self):
		return self.places.pop()


class Queue:

	def __init__(self):
		self.queue = []

	def __str__(self):
		return '<back> [{}] <front>'.format(', '.join(map(str, self.queue)))

	def __bool__(self):
		return bool(self.queue)

	def __len__(self):
		return len(self.queue)

	def append(self, obj):
		self.queue.insert(0, obj)
		return self

	def take(self):
		return self.queue.pop() if self.queue else None

	def replace(self, old_idx, new_idx):
		old = self.queue[old_idx]
		new = self.queue[old_idx]
		self.queue.remove(old)
		self.queue.remove(new)
		self.queue.insert(new_idx, old)
		self.queue.insert(old_idx, new)

	def empty(self):
		return not self.queue

	def clear(self):
		self.queue.clear()


class Vehicle:

	def __init__(self, brand, goods, count, from_):
		self.brand = brand
		self.goods_from = from_
		self.goods = goods
		self.count = count

	def __str__(self):
		return '"{}" with "{}"'.format(self.brand, self.goods)


class Customs:

	def __init__(self):
		self.queue = Queue()
		self.workers = {
			'Orange': 'Ivan',
			'Banana': 'Roman',
			'Tesla Model X': 'Ilon Mask'
		}

	def __bool__(self):
		return not self.queue.empty()

	def add_vehicle(self, vehicle):
		self.queue.append(vehicle)

	def call_worker(self, goods):
		return self.workers[goods]

	def check_next(self):
		vehicle = self.queue.take()
		worker = self.call_worker(vehicle.goods)
		print('{} is checked by {}'.format(vehicle, worker))


def main():
	c = Customs()

	c.add_vehicle(Vehicle('Volvo', 'Orange', 256, 'Turkey'))
	c.add_vehicle(Vehicle('Mercedes', 'Banana', 128, 'Africa'))
	c.add_vehicle(Vehicle('Volvo', 'Tesla Model X', 7, 'Odesa'))

	while c:
		c.check_next()


if __name__ == '__main__':
	main()
