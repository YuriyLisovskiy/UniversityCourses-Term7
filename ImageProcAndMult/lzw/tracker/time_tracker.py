import time


class TrackingValue:

	def __init__(self, start_time):
		self._start_time = start_time
		self._time_passed = 0.0

	def increase(self):
		self._time_passed += float('%s' % (time.time() - self._start_time))

	def __str__(self):
		return '{} sec'.format(self._time_passed)


class TimeTracker:

	def __init__(self):
		self._values = {}

	def start(self, value):
		self._values[value] = TrackingValue(time.time())

	def track(self, value):
		if value not in self._values:
			raise ValueError('tracking is not started for "{}"'.format(value))
		self._values[value].increase()

	def __str__(self):
		return '\n'.join(['{}: {}'.format(key, val) for key, val in self._values.items()])
