import os
import json

from app.settings import BASE_DIR


# Dict-based storage.
class Storage:
	
	def __init__(self):
		self.storage = self._load()
	
	def _find(self, typ_, user_id, course_name):
		if str(user_id) not in self.storage:
			return None
		data = self.storage[str(user_id)][typ_]
		for item in data:
			current = set(item['name'].lower().split())
			passed = set(course_name.lower().split())
			if current.issubset(passed) or current.issuperset(passed):
				return item
		return None
	
	@staticmethod
	def _load():
		file_path = '{}/storage.json'.format(BASE_DIR)
		if os.path.exists(file_path):
			with open(file_path, 'r') as fp:
				return json.load(fp)
		else:
			return {}
	
	def _save(self):
		with open('{}/storage.json'.format(BASE_DIR), 'w') as fp:
			json.dump(self.storage, fp)
	
	def add_user(self, user_id):
		self.storage[str(user_id)] = {
			'exams': [],
			'credits': []
		}
		self._save()
	
	def has_user(self, user_id):
		return str(user_id) in self.storage
	
	def has_exam(self, user_id, exam_info):
		return self._find('exams', user_id, exam_info[0].strip().lower()) is not None
	
	def has_credit(self, user_id, credit_info):
		return self._find('credits', user_id, credit_info[0].strip().lower()) is not None
	
	def add_credit(self, user_id, new_credit):
		self.storage[str(user_id)]['credits'].append({
			'name': new_credit[0].strip(),
			'date': new_credit[1].strip(),
			'time': new_credit[2].strip()
		})
		self._save()
	
	def add_exam(self, user_id, new_exam):
		self.storage[str(user_id)]['exams'].append({
			'name': new_exam[0].strip(),
			'date': new_exam[1].strip(),
			'time': new_exam[2].strip()
		})
		self._save()
	
	def get_exam_info(self, user_id, exam_name):
		exam = self._find('exams', user_id, exam_name.strip().lower())
		if not exam:
			return None
		return '{} is an exam, it will be held on {} at {}'.format(
			exam['name'],
			exam['date'],
			exam['time']
		)
	
	def get_credit_info(self, user_id, credit_name):
		credit = self._find('credits', user_id, credit_name.strip().lower())
		if not credit:
			return None
		return '{} is a credit, it will be held on {} at {}'.format(
			credit['name'],
			credit['date'],
			credit['time']
		)

	def get_exams(self, user_id):
		return '\n'.join(['{}) {}'.format(idx + 1, x['name']) for idx, x in enumerate(
			self.storage[str(user_id)]['exams']
		)])
	
	def get_courses(self, user_id):
		exams = self.storage[str(user_id)]['exams']
		credits_ = self.storage[str(user_id)]['credits']
		return '\n'.join(['{}) {}'.format(idx + 1, x['name']) for idx, x in enumerate(credits_ + exams)])
	
	def print(self):
		print(json.dumps(self.storage, sort_keys=True, indent=4))
