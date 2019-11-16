#include <iostream>
#include <functional>

template <typename T, typename Func>
Func if_else(const std::function<bool()>& cond, Func success, Func fail)
{
	// Closure: returns lambda as a result of 'if_else' function
	return [cond, success, fail]() -> T {
		return cond() ? success() : fail();
	};
}

// Higher-order functions: passing lambdas
//  and if_else function as parameter of if_else.
int bin_search(int arr[], int n, int x)
{
	// Encapsulation: hide 'inner' variable
	//  (lambda function) in bin_search function
	std::function<int(int*, int, int, int)> inner = [&](int arr[], int x, int bottom, int top)
	{
		int mid = (top + bottom) / 2;
		return if_else<int, std::function<int()>>(
			[top, bottom]() -> bool { return top < bottom; },
			[]() -> int { return -1; },
			if_else<int, std::function<int()>>(
				[arr, mid, x]() -> bool { return arr[mid] == x; },
				[mid]() -> int { return mid; },
				if_else<int, std::function<int()>>(
					[arr, mid, x]() -> bool { return arr[mid] > x; },
					[inner, arr, x, bottom, mid]() -> int { return inner(arr, x, bottom, mid - 1); },	// Recursion
					[inner, arr, x, top, mid]() -> int { return inner(arr, x, mid + 1, top); }			// Recursion
				)
			)
		)();
	};
	return inner(arr, x, 0, n - 1);
}


int main()
{
	int n = 7;
	int arr[] = {2, 5, 7, 9, 11, 17, 222};
	std::cout << bin_search(arr, n, 11) << '\n';
	std::cout << bin_search(arr, n, 12) << '\n';

	return 0;
}
