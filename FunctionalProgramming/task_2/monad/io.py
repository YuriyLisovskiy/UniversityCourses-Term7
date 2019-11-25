# IO monad allows us to write a sequence of side-effecting instructions
# (including I/O), even though we are working with pure values only.


# Base IO monad class.
class IO:

	@staticmethod
	def ret(val):
		return IOReturn(val)

	@staticmethod
	def print(str_to_print, end='\n'):
		return IOPrint(str_to_print, end)

	@staticmethod
	def read():
		return IORead()

	def bind(self, func):
		return IOBind(self, func)

	def run(self):
		if isinstance(self, IOBind):
			# Executes nested @io_monad.
			val = self.io_monad.run()

			# applies bound function to the result and
			# runs IO monad which is returned from self.bind_func(...).
			return self.bind_func(val).run()

		# If self is IOResult, simply returns the value it holds.
		if isinstance(self, IOReturn):
			return self.val

		# Just prints given string.
		if isinstance(self, IOPrint):
			print(self.str_to_print, end=self.end)
			return None

		# Calls console input.
		if isinstance(self, IORead):
			return input()


# Used for applying a function to a result of @io_monad's run() method.
class IOBind(IO):

	def __init__(self, io_monad, bind_func):
		self.io_monad = io_monad
		self.bind_func = bind_func


# Used for returning an actual value from IO monad instance.
class IOReturn(IO):

	def __init__(self, val):
		self.val = val


# Outputs given string to a terminal window.
class IOPrint(IO):

	def __init__(self, str_to_print, end='\n'):
		self.str_to_print = str_to_print
		self.end = end


# Used for console input.
class IORead(IO):
	pass
