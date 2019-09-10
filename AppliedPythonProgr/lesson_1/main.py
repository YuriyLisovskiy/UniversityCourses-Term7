"""
R = float(input('Радіус кола? '))

import math
d = 2 * math.pi * R

print('Радіус кола = ', R)
print('Довжина кола = ', d)
"""


"""
a = 3
print(a)

a = 'good weather'
print(a)

a = 1.23
print(a)
"""


"""
a = 12345678901234567890123456789012345678901234567890
b = 1

print(a + b)
"""


"""
one, *two = 'join'
print(one, two)
"""


"""
a = 1
b = 2

k = 2*a+b if a > b else 3*a-4 if a == b else 4*a+5

print(k)
"""


"""
p = int(input('Ціле число більше за 1: '))
x = p // 2
while x > 1:
	if p % x == 0:
		print(p, 'має дільник', x, '- не є простим')
		break
	x -= 1
else:
	print(p, 'просте')
"""


"""
def generator(begin, end, step=0.1):
	while begin < end:
		yield round(begin, 1)
		begin += step


print(list(range(1, 10, 1)))

"""


"""
words = ['cat', 'window', 'defenestrate']
for w in words:
	print(w, len(w))
"""


"""
for i in range(10, 300):
	if i < 100:
		des, od = i // 10 % 10, i % 10; if des == od: print(i)
	else:
		sot, des, od = i // 100, i // 10 % 10, i % 10
		if sot == des or sot == od or des == od:
			print(i)
"""


"""
t = 'good weather'
print(t)

t = "good weather"
print(t)

t = '''good weather'''
print(t)

t = \"""good weather""\"
print(t)
"""


"""
l = '''Ми будемо гарно вчитися
Від початку до кінця
А як сесія настане
Буде радість ще й яка'''

print(l)
"""


# for lt in range(ord('A'), ord('Z')+1): print(lt, chr(lt))


"""
p = 'unfortunately'

for i in range(len(p)-1):
	print(p[i:i+2])
"""


# Подвоїти голосні літери
g = 'аоуеиі'
s = 'Програмування'

i = 0
while i < len(s):
	if s[i] in g:
		s = s.replace(s[i], s[i] * 2)
		i += 1
	i += 1

print(s)
