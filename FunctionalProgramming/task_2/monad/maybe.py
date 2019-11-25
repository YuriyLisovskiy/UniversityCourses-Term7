
class Maybe:

	def __init__(self, value):
		self._value = value

	@staticmethod
	def some(value):
		if value is None:
			raise Exception('provided value must not be empty')
		return Maybe(value)

	@staticmethod
	def none():
		return Maybe(None)

	@staticmethod
	def from_value(value):
		if value is None:
			return Maybe.none()
		return Maybe.some(value)

	def get_or_else(self, default):
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

	def ap(self, monad):
		monad.map(self._value)
