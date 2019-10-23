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
func binSearchInner(arr []int, x int, bottom int, top int) int {
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
				return arr[mid] == x
			},
			func() interface{} {
				return mid
			},
			ifElse(
				func() bool {
					return arr[mid] > x
				},
				func() interface{} {
					return binSearchInner(arr, x, bottom, mid - 1)	// Recursion
				},
				func() interface{} {
					return binSearchInner(arr, x, mid + 1, top)		// Recursion
				},
			),
		),
	)().(int)
}

func binSearch(arr []int, x int) int {
	return binSearchInner(arr, x, 0, len(arr) - 1)
}

func main() {
	arr := []int {2, 5, 7, 9, 11, 17, 222}
	println(binSearch(arr, 11))
	println(binSearch(arr, 12))
}
