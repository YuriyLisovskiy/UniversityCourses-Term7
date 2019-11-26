# Maybe monad represents computations which has a risk go wrong
# because of applying functions to None values. Methods of Maybe class
# ensure that passed function will not be called if parameter's
# value is None.


# Maybe monad class.
class Maybe:

	def __init__(self, value):
		self._value = value

	# Returns Maybe instance initialized with given value.
	# Ensures that @value is not None.
	@staticmethod
	def some(value):
		if value is None:
			raise Exception('provided value must not be empty')
		return Maybe(value)

	# Initializes and returns Maybe with None.
	# Result of any operation applied to such object
	#   returns Maybe(None) result.
	@staticmethod
	def none():
		return Maybe(None)

	# Returns new Maybe instance from given value.
	@staticmethod
	def from_value(value):
		if value is None:
			return Maybe.none()
		return Maybe.some(value)

	# Retrieves an actual value from monad instance,
	#   or @default if monad's value is None.
	def get_or_else(self, default):
		if self._value is None:
			return default
		return self._value

	# Applies @fn function to an actual value of current monad
	#   and builds new Maybe instance from @fn result
	#   if self._value is not None, otherwise returns Maybe(None).
	# @fn must return non-Maybe result.
	def map(self, fn):
		if self._value is None:
			return Maybe.none()
		return Maybe.from_value(fn(self._value))

	# Applies @fn function to an actual value of current monad
	#   and @fn result if self._value is not None, otherwise returns Maybe(None).
	# @fn must return Maybe result.
	def flat_map(self, fn):
		if self._value is None:
			return Maybe.none()
		return fn(self._value)
