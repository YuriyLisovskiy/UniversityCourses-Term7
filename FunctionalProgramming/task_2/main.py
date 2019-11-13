"""
class Option:

	def __init__(self, value):
		self._value = value

	def map(self, fn):
		return self.match(
			lambda val: Some(fn(val)),
			lambda: _None()
		)

	def flat_map(self, fn):
		return self.match(
			lambda val: fn(val),
			lambda: _None()
		)

	def filter(self, fn):
		if fn(self._value):
			return Some(self._value)
		return None

	def match(self, some, none):
		if self._value is None:
			return none()
		return some(self._value)


class Some(Option):

	def __init__(self, value):
		if value is None:
			raise ValueError('provided value must not be empty')
		super().__init__(value)


class _None(Option):

	def __init__(self):
		super().__init__(None)


class Either:

	def __init__(self, left, right):
		self._left = left
		self._right = right
		self._is_left = False
		self._is_right = False

	@staticmethod
	def left(value):
		return Left(value)

	@staticmethod
	def right(value):
		return Right(value)

	@staticmethod
	def of(value):
		return Either.right(value)

	def map(self, fn):
		raise NotImplementedError

	def get_or_else(self, default):
		raise NotImplementedError


class Left(Either):

	def __init__(self, value):
		super().__init__(value, None)
		super()._is_left = True

	def map(self, fn):
		return self

	def get_or_else(self, default):
		raise default


class Right(Either):

	def __init__(self, value):
		super().__init__(None, value)
		self._is_right = True

	def map(self, fn):
		return Either.of(fn(self._right))

	def get_or_else(self, default):
		raise self._right
"""


class Maybe:

	def __init__(self, value):
		self._value = value

	def __eq__(self, other):
		return self._value == other._value

	def __gt__(self, other):
		return self._value > other._value

	def __lt__(self, other):
		return self._value < other._value

	@staticmethod
	def some(value):
		if value is None:
			raise ValueError('provided value must not be empty')
		return Maybe(value)

	@staticmethod
	def none():
		return Maybe(None)

	@staticmethod
	def from_value(value):
		if value is None:
			return Maybe.none()
		return Maybe.some(value)

	def get_or_default(self, default):
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


def if_else(cond, success, fail):
	def inner():
		return success() if cond() else fail()

	return inner


def bin_search(arr, x):
	def get_arr_item(arr_, idx):
		return arr_.flat_map(lambda arr_val: idx.map(lambda mid_val: arr_val[mid_val]))

	def compare(left, right, cmp_fn, default):
		maybe = left.flat_map(lambda left_val: right.map(lambda right_val: cmp_fn(left_val, right_val)))
		return maybe.get_or_default(default)

	def m_sum(first, second):
		return first.flat_map(lambda first_val: second.map(lambda second_val: first_val + second_val))

	def inner(arr_, x_, bottom, top):
		mid = m_sum(top, bottom).map(lambda sum_: sum_ // 2)
		return if_else(
			lambda: compare(top, bottom, lambda _l, _r: _l < _r, default=True),
			lambda: Maybe.none(),
			if_else(
				lambda: compare(get_arr_item(arr_, mid), x_, lambda _l, _r: _l == _r, default=False),
				lambda: mid,
				if_else(
					lambda: compare(get_arr_item(arr_, mid), x_, lambda _l, _r: _l > _r, default=True),
					lambda: inner(arr_, x_, bottom, mid.map(lambda val: val - 1)),
					lambda: inner(arr_, x_, mid.map(lambda val: val + 1), top)
				)
			)
		)()

	maybe_arr = Maybe.from_value(arr)
	return inner(
		maybe_arr, Maybe.from_value(x), Maybe.from_value(0), maybe_arr.map(lambda val: len(val) - 1)
	).get_or_default('Item {} is not found'.format(x))


def main():
	ls = (2, 5, 7, 9, 11, 17, 222)
	print(bin_search(ls, 11))
	print(bin_search(ls, 12))


if __name__ == '__main__':
	main()
