from monad import Maybe


def if_else(cond, success, fail):
	def inner():
		return success() if cond() else fail()

	return inner


def bin_search(arr, x):

	# Returns Maybe instance from @arr_ by @idx.
	# @arr_ and @idx are Maybe instances.
	def get_arr_item(arr_, idx):
		return arr_.flat_map(
			lambda arr_val: idx.map(
				lambda mid_val: arr_val[mid_val]
			)
		)

	# Compares two Maybe instances' actual values using @cmp_fn.
	# Returns boolean result of comparison, or default if any of
	#   left/right/cmp_fn returns None.
	def maybe_compare(left, right, cmp_fn, default):
		maybe = left.flat_map(
			lambda left_val: right.map(
				lambda right_val: cmp_fn(left_val, right_val)
			)
		)
		return maybe.get_or_else(default)

	# Calculates sum of two Maybe instances' actual values.
	# Returns Maybe instance witch contains first+second result.
	def maybe_sum(first, second):
		return first.flat_map(
			lambda first_val: second.map(
				lambda second_val: first_val + second_val
			)
		)

	# Recursive function which searches for @x_ in @arr_.
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

	# Warps actual values with Maybe monad.
	maybe_arr = Maybe.from_value(arr)
	return inner_search(
		maybe_arr, Maybe.from_value(x), Maybe.from_value(0), maybe_arr.map(lambda val: len(val) - 1)

		# if inner_search returns Maybe(None), return a message that element is not found.
	).get_or_else('Item {} is not found'.format(x))


if __name__ == '__main__':
	ls = [2, 5, 7, 9, 11, 17, 222]
	print(bin_search(ls, 11))
	print(bin_search(None, 5))
	print(bin_search(ls, None))
	print(bin_search(ls, 12))
