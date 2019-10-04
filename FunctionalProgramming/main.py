def f1(x):
	return x + 1


def f2(x):
	return x + 2


def f3(x):
	return x + 3


def unit(x):
	return x, [x]


def bind(t, f):
	res = f(t[0])
	return res, t[1] + [res]


if __name__ == '__main__':
	print(bind(bind(bind(unit(1), f1), f2), f3))
