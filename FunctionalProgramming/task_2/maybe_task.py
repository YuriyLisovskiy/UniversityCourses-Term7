
class Maybe:

	def __init__(self, value):
		self._value = value

	@staticmethod
	def some(value):
		if value is None:
			raise Exception('provided value must not be empty')
		return Maybe(value)

	@staticmethod
	def none():
		return Maybe(None)

	@staticmethod
	def from_value(value):
		if value is None:
			return Maybe.none()
		return Maybe.some(value)

	def get_or_else(self, default):
		if self._value is None:
			return default
		return self._value

	def map(self, fn):
		if self._value is None:
			return Maybe.none()
		return Maybe.from_value(fn(self._value))

	def flat_map(self, fn):
		if self._value is None:
			return Maybe.none()
		return fn(self._value)

	def ap(self, monad):
		monad.map(self._value)


def if_else(cond, success, fail):
	def inner():
		return success() if cond() else fail()

	return inner


def bin_search(arr, x):
	def get_arr_item(arr_, idx):
		return arr_.flat_map(lambda arr_val: idx.map(lambda mid_val: arr_val[mid_val]))

	def maybe_compare(left, right, cmp_fn, default):
		maybe = left.flat_map(lambda left_val: right.map(lambda right_val: cmp_fn(left_val, right_val)))
		return maybe.get_or_else(default)

	def maybe_sum(first, second):
		return first.flat_map(lambda first_val: second.map(lambda second_val: first_val + second_val))

	def inner_search(arr_, x_, bottom, top):
		mid = maybe_sum(top, bottom).map(lambda sum_: sum_ // 2)
		return if_else(
			lambda: maybe_compare(top, bottom, lambda _l, _r: _l < _r, default=True),
			lambda: Maybe.none(),
			if_else(
				lambda: maybe_compare(get_arr_item(arr_, mid), x_, lambda _l, _r: _l == _r, default=False),
				lambda: mid,
				if_else(
					lambda: maybe_compare(get_arr_item(arr_, mid), x_, lambda _l, _r: _l > _r, default=True),
					lambda: inner_search(arr_, x_, bottom, mid.map(lambda val: val - 1)),
					lambda: inner_search(arr_, x_, mid.map(lambda val: val + 1), top)
				)
			)
		)()

	maybe_arr = Maybe.from_value(arr)
	return inner_search(
		maybe_arr, Maybe.from_value(x), Maybe.from_value(0), maybe_arr.map(lambda val: len(val) - 1)
	).get_or_else('Item {} is not found'.format(x))


def main():
	ls = [2, 5, 7, 9, 11, 17, 222]
	print(bin_search(ls, 11))
	print(bin_search(None, 5))
	print(bin_search(ls, None))
	print(bin_search(ls, 12))


if __name__ == '__main__':
	main()
