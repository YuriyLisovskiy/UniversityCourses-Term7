

class Human:

	MALE = 'male'
	FEMALE = 'female'

	def __init__(self, name, age, gender):
		self.name = name
		self.age = age
		self.gender = gender

	def __str__(self):
		return '{} is {}, {} years old'.format(self.name, self.gender, self.age)

	def __eq__(self, other):
		return self.name == other.name and self.gender == other.gender and self.age == other.age

	def __lt__(self, other):
		return self.age < other.age

	def __gt__(self, other):
		return self.age > other.age

	def get_name(self):
		return self.name

	def get_age(self):
		return self.name

	def get_gender(self):
		return self.name


if __name__ == '__main__':
	john = Human('John', 20, Human.MALE)
	kate = Human('Kate', 21, Human.FEMALE)
	stephan = Human('Stephan', 20, Human.MALE)
	[print(human) for human in [john, kate]]
	print(kate < john)
	print(kate > john)
	print(stephan == john)
	print(john == john)
