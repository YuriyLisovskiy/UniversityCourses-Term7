
def if_else(cond, success, fail):
	# Closure: returns inner function as a result of 'if_else' function
	def inner():
		return success() if cond() else fail()
	return inner


# Higher-order functions: passing lambdas
#  and if_else function as parameter of if_else.
def bin_search_inner(arr, x, bottom, top):
	mid = (top + bottom) // 2
	return if_else(
		lambda: top < bottom,
		lambda: -1,
		if_else(
			lambda: arr[mid] == x,
			lambda: mid,
			if_else(
				lambda: arr[mid] > x,
				lambda: bin_search_inner(arr, x, bottom, mid - 1),  # Recursion
				lambda: bin_search_inner(arr, x, mid + 1, top)      # Recursion
			)
		)
	)()


def bin_search(arr, x):
	return bin_search_inner(arr, x, 0, len(arr) - 1)


if __name__ == '__main__':
	ls = [2, 5, 7, 9, 11, 17, 222]
	print(bin_search(ls, 11))
	print(bin_search(ls, 12))
