import math

from monad import Try


# Gets number from console as float.
def input_number(number_name):

	# recover will be called in case of input_number failure,
	#   i.e. when user types non-numeric string.
	def recover(exc):
		print(exc)
		return input_number(number_name)

	print('Input {}: '.format(number_name), end='')

	# user input
	return Try.of_failable(input).map(
		lambda val: float(val)    # cast string to float
	).recover(
		lambda exc: recover(exc)  # print exception if input string is not numeric
	)


if __name__ == '__main__':

	number = input_number('number')
	base = input_number('base')
	denominator = input_number('denominator')

	# Calculates log(number, base) / denominator
	Try.of_failable(

		# number can be less or equal to zero which causes the domain error.
		# base can be less than zero which also causes the domain error.
		lambda: math.log(number, base)
	).map(

		# denominator can be 0, division by zero causes an exception.
		lambda log_res: log_res / denominator
	).map(

		# Print the result of above calculation.
		lambda result: print('Result is {}'.format(result))
	).recover(

		# Handle the generated exception.
		lambda exc: print(exc)
	)
