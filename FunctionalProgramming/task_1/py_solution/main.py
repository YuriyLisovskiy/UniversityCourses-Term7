
def if_else(cond, success, fail):
	# Closure: returns inner function as a result of 'if_else' function
	def inner():
		return success() if cond() else fail()

	return inner


# Higher-order functions: passing lambdas
#  and if_else function as parameter of if_else.
def bin_search(arr, x):
	# Encapsulation: hide 'inner' helper function
	#   in bin_search function
	def inner(arr_, x_, bottom, top):
		mid = (top + bottom) // 2
		return if_else(
			lambda: top < bottom,
			lambda: -1,
			if_else(
				lambda: arr_[mid] == x_,
				lambda: mid,
				if_else(
					lambda: arr_[mid] > x_,
					lambda: inner(arr_, x_, bottom, mid - 1),  # Recursion
					lambda: inner(arr_, x_, mid + 1, top)      # Recursion
				)
			)
		)()

	return inner(arr, x, 0, len(arr) - 1)


if __name__ == '__main__':
	ls = [2, 5, 7, 9, 11, 17, 222]
	print(bin_search(ls, 11))
	print(bin_search(ls, 12))
