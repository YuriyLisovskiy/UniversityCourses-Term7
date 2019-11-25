from monad import IO


# Returns IOResult monad instance with calculated result.
def factorial(x):
	if x == 0:

		# Return IOResult instance witch contains 1.
		return IO.ret(1)
	return IO.ret(x).bind(

		# Recursive call of factorial() function.
		lambda val: factorial(x - 1).bind(

			# Return IOResult with calculated value in recursive call.
			lambda rec_val: IO.ret(val * rec_val)
		)
	)


def get_int():
	# Print input hint.
	return IO.print('Input number: ', end='').bind(

		# Lambda function to read number from console.
		lambda _: IO.read().bind(

			# Return IOReturn monad with casted input to integer.
			lambda inp: IO.ret(int(inp)) if inp.isdigit() else get_int()
		)
	)


if __name__ == '__main__':

	# Calculates factorial using user-input number.
	get_int().bind(

		# Calculate factorial from get_int() result.
		lambda digit: factorial(digit).bind(

			# Bind lambda function to print result.
			lambda result: IO.print('Factorial of {} is {}'.format(digit, result))
		)
	).run()

	# Calculates factorial of hardcoded number.
	number = 13
	factorial(number).bind(

		# Bind lambda function to print result.
		lambda result: IO.print('Factorial of {} is {}'.format(number, result))
	).run()
