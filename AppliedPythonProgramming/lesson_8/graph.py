class Graph:

	def __init__(self, src_collection=None):
		if not src_collection:
			self.graph = {}
		else:
			self.graph = dict(src_collection)

	def __str__(self):
		return '{{\n{}\n}}'.format(',\n'.join(map(lambda x: '   {}: {}'.format(x[0], x[1]), self.graph.items())))

	def get_graph(self):
		return self.graph

	def from_file(self, file):
		self.graph.clear()
		with open(file, 'r') as f:
			for line in f:
				item = line.rstrip().split(':')
				self.graph[item[0]] = item[1].split(',')
			# res = self.correct()
			# return res

	def save_to_file(self, file):
		with open(file, 'w') as f:
			for elem in list(self.graph.items()):
				f.write('{}: {}\n'.format(elem[0], ','.join(map(str, elem[1]))))

	def get(self, key):
		return self.graph.get(key)

	def set(self, key, val):
		if isinstance(val, list):
			self.graph[key] = val
		else:
			self.graph[key] = [val]

	def remove(self, key):
		if key in self.graph:
			del self.graph[key]

	def correct(self):
		test = True
		list_err = []

		# Check for isolated vertices
		for k in self.graph.keys():
			if len(self.graph[k]) == 0:
				list_err.append('Error: empty values: {}: {}'.format(k, self.graph.get(k)))
				test = False
				break

		# Check for ...
		# ...
		return test, list_err
