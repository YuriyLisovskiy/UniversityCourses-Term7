from lesson_8.graph import Graph


def solution(graph, city):
	first_stops = graph.get(city)
	second_stops = [graph.get(val) for val in first_stops]

	print(Graph(zip([city], [first_stops])))
	print(Graph(zip(first_stops, second_stops)))


if __name__ == '__main__':
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

	g = Graph(grouped)
	print(g)
	solution(g, 'Київ')
