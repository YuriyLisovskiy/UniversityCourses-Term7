from lesson_8.graph import Graph


"""
def solution(graph, city):
	first_stops = graph.get(city)
	second_stops = [graph.get(val) for val in first_stops]

	print(Graph(zip([city], [first_stops])))
	print(Graph(zip(first_stops, second_stops)))
"""


def print_solution(dist, n, src):
	for node in range(n):
		print('from', src, 'to', node, '-', dist[node])


def task_1():
	data = [
		'Львів', 'Київ', 'Мукачево', 'Ужгород', 'Івано-Франківськ', 'Тернопіль'
	]

	grouped = []
	for x in range(len(data)):
		grouped.append(
			(
				data[x],
				[data[(k + x + 3) % len(data)] for k in range(len(data)) if data[x] != data[(k + x + 3) % len(data)]]
			)
		)


if __name__ == '__main__':
	matrix = [
		[0, 2, 0, 0, 0, 0, 1],
		[0, 0, 10, 0, 0, 0, 3],
		[0, 0, 0, 6, 0, 0, 0],
		[0, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[4, 0, 0, 0, 5, 0, 0],
		[0, 0, 2, 4, 8, 2, 0]
	]

	src_vertex = 2

	g = Graph(matrix)

	solution = g.dijkstra(src_vertex)

	print_solution(solution, len(matrix), src_vertex)
