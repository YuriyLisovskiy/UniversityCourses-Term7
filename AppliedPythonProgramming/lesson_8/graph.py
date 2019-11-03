import sys


class Graph:

	def __init__(self, src_collection=None):
		self.is_weighted = False
		if not src_collection:
			self.graph = {}
		elif isinstance(src_collection, (list, tuple)):
			self.is_weighted = True
			self.graph = {}
			for idx, row in enumerate(src_collection):
				assert isinstance(row, (list, tuple))
				self.graph[idx] = [(pos, x) for pos, x in enumerate(row)]
		else:
			self.graph = dict(src_collection)

	def __str__(self):
		return '{{\n{}\n}}'.format(',\n'.join(map(lambda x: '   {}: {}'.format(x[0], x[1]), self.graph.items())))

	def __len__(self):
		return len(self.graph)

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

	def min_distance(self, dist, spt_set):
		minimum = sys.maxsize
		for v in range(len(self.graph)):
			if dist[v] <= minimum and not spt_set[v]:
				minimum = dist[v]
				min_index = v

		# noinspection PyUnboundLocalVariable
		return min_index

	def dijkstra(self, src):
		dist = [sys.maxsize] * len(self.graph)
		dist[src] = 0
		spt_set = [False] * len(self.graph)
		for _ in range(len(self.graph)):
			u = self.min_distance(dist, spt_set)

			# shortest path tree
			spt_set[u] = True
			for v in range(len(self.graph)):
				if self.get(u)[v][1] > 0 and not spt_set[v] and dist[v] > dist[u] + self.get(u)[v][1]:
					dist[v] = dist[u] + self.get(u)[v][1]
		return [d if d != sys.maxsize else 'No path' for d in dist]
