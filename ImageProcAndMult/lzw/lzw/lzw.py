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
	"""Compress a string to a list of output symbols."""

	# Build the dictionary.
	dict_size = 256
	dictionary = dict((str(i), i) for i in range(dict_size))
	# in Python 3: dictionary = {chr(i): i for i in range(dict_size)}

	result = []
	s = str(uncompressed.pop(0))
	for item in uncompressed:
		c = str(item)
		sc = '{}+{}'.format(s, c)
		if sc in dictionary:
			s = sc
		else:
			result.append(dictionary[s])
			# Add wc to the dictionary.
			dictionary[sc] = dict_size
			dict_size += 1
			s = c

	# Output the code for w.
	if s:
		result.append(dictionary[s])
	return result


def decompress(compressed):
	"""Decompress a list of output ks to a string."""

	# Build the dictionary.
	dict_size = 256
	dictionary = {str(i): str(i) for i in range(dict_size)}

	result = []
	old = compressed.pop(0)
	s = dictionary[str(old)]
	c = s[0]
	result.append(dictionary[str(old)])
	for new in compressed:
		if str(new) not in dictionary:
			s = dictionary[str(old)]
			s += c
		else:
			# raise ValueError('Bad compressed k: %s' % k)
			s = dictionary[str(new)]

		result.append(int(s))

		c = ""
		c += s[0]

		# Add w+entry[0] to the dictionary.
		dictionary[dict_size] = '{}{}'.format(dictionary[str(old)], c)
		dict_size += 1
		old = new
	return result
