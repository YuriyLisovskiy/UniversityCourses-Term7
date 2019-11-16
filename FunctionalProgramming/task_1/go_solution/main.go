package main

func ifElse(cond func() bool, success func() interface{}, fail func() interface{}) func() interface{} {
	// Closure: returns anonymous function as a result of 'ifElse'
	return func() interface{} {
		if cond() {
			return success()
		}
		return fail()
	}
}

// Higher-order functions: passing anonymous functions
// 	and 'ifElse' as parameters of 'ifElse'.
func binSearch(arr []int, x int) int {
	// Encapsulation: hide 'inner' helper function
	//   in 'binSearch' function
	var inner func(arr_ []int, x_ int, bottom int, top int) int
	inner = func (arr_ []int, x_ int, bottom int, top int) int {
		mid := (top + bottom) / 2
		return ifElse(
			func() bool {
				return top < bottom
			},
			func() interface{} {
				return -1
			},
			ifElse(
				func() bool {
					return arr_[mid] == x_
				},
				func() interface{} {
					return mid
				},
				ifElse(
					func() bool {
						return arr_[mid] > x_
					},
					func() interface{} {
						return inner(arr_, x_, bottom, mid - 1)	// Recursion
					},
					func() interface{} {
						return inner(arr_, x_, mid+1, top)		// Recursion
					},
				),
			),
		)().(int)
	}

	return inner(arr, x, 0, len(arr) - 1)
}

func main() {
	arr := []int {2, 5, 7, 9, 11, 17, 222}
	println(binSearch(arr, 11))
	println(binSearch(arr, 12))
}
