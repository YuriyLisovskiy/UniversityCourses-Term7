"""
def compress(uncompressed):
	# Compress a string to a list of output symbols.

	# Build the dictionary.
	dict_size = 256
	dictionary = dict((str(i), i) for i in range(dict_size))
	# in Python 3: dictionary = {chr(i): i for i in range(dict_size)}

	w = ""
	result = []
	for c in uncompressed:
		wc = w + str(c)
		if wc in dictionary:
			w = wc
		else:
			if w in dictionary:
				result.append(dictionary[w])
			# Add wc to the dictionary.
			dictionary[wc] = dict_size
			dict_size += 1
			w = str(c)

	# Output the code for w.
	if w:
		result.append(dictionary[w])
	return result
"""


def compress(uncompressed):
	dict_size = 256
	dictionary = {str(i): i for i in range(dict_size)}

	result = []
	s = str(uncompressed.pop(0))
	for item in uncompressed:
		c = str(item)
		sc = '{}+{}'.format(s, c)
		if sc in dictionary:
			s = sc
		else:
			result.append(dictionary[s])
			dictionary[sc] = dict_size
			dict_size += 1
			s = c
	if s:
		result.append(dictionary[s])
	return result


def str_to_list(s):
	return [int(x) for x in s.split(',')]


def decompress(compressed):
	dict_size = 256
	dictionary = {str(i): str(i) for i in range(dict_size)}

	result = []
	old = compressed.pop(0)
	c = old
	result.append(old)
	for new in compressed:
		if str(new) in dictionary:
			s = dictionary[str(new)]
		else:
			s = dictionary[str(old)]
			if c != '':
				s = '{},{}'.format(s, c)

		part = str_to_list(s)

		result += part

		c = s.split(',')[0]

		dictionary[str(dict_size)] = '{},{}'.format(str(old), c)
		dict_size += 1
		old = new
	return result
